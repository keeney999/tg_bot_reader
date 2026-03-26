import io
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from src.handlers.commands import ScanState
from src.services.image_utils import load_image_from_bytes
from src.services.ocr import extract_barcodes, extract_order_numbers
from src.services.sheets import append_to_sheet
from src.utils.logger import logger
from src.models.schemas import ScanResult
from src.config import GROUP_ID, TOPIC_ID, ONLY_GROUP, ONLY_TOPIC

router = Router()

@router.message(ScanState.waiting_for_photo, F.photo)
async def handle_photo(message: Message, bot:Bot, state: FSMContext):
    # Если бот ограничен группой/темой, проверяем
    if ONLY_GROUP and message.chat.id != GROUP_ID:
        await message.answer("Этот бот работает только в определённой группе.")
        await state.clear()
        return
    if ONLY_TOPIC and message.message_thread_id != TOPIC_ID:
        await message.answer("Используй тему «ШК» для сканирования.")
        await state.clear()
        return

    # 1. Скачиваем фото
    photo_file = await bot.get_file(message.photo[-1].file_id)
    image_bytes = io.BytesIO()
    await bot.download_file(photo_file.file_path, destination=image_bytes)
    image = load_image_from_bytes(image_bytes)

    # 2. Распознаём
    barcodes = extract_barcodes(image)
    order_numbers = extract_order_numbers(image)

    # 3. Формируем ответ
    answer = []
    if barcodes:
        answer.append("🔢 Штрихкоды:\n" + "\n".join(barcodes))
    else:
        answer.append("❌ Штрихкоды не найдены")
    if order_numbers:
        answer.append("📦 Номера заказов:\n" + "\n".join(order_numbers))
    else:
        answer.append("❌ Номера заказов не найдены")

    await message.reply("\n\n".join(answer))

    # 4. Сохраняем в Google Sheets
    scan_result = ScanResult(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        order_numbers=order_numbers,
        barcodes=barcodes,
        message_link=f"https://t.me/c/{message.chat.id}/{message.message_id}?thread={message.message_thread_id}"
    )
    append_to_sheet(scan_result)
    logger.info(f"Processed photo from {message.from_user.id}")

    # 5. Завершаем состояние
    await state.clear()

@router.message(ScanState.waiting_for_photo)
async def handle_wrong_input(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, отправь именно фотографию (картинку).")