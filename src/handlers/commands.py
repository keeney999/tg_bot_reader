from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

class ScanState(StatesGroup):
    waiting_for_photo = State()

# Кнопка для активации (удобно в группе)
scan_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📸 Отсканировать")]],
    resize_keyboard=True,
    one_time_keyboard=True
)

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот для распознавания штрихкодов и номеров заказов.\n"
        "Используй команду /scan или кнопку «Отсканировать», чтобы начать.",
        reply_markup=scan_keyboard
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📌 Как пользоваться:\n"
        "1. Нажми /scan или кнопку «Отсканировать»\n"
        "2. Отправь фото с товаром (на нём должны быть видны штрихкод и номер заказа)\n"
        "3. Бот распознает данные и запишет их в Google Таблицу\n\n"
        "Формат номера заказа: 12345678-9012-3"
    )

@router.message(Command("scan"))
async def cmd_scan(message: Message, state: FSMContext):
    await state.set_state(ScanState.waiting_for_photo)
    await message.answer(
        "Отправь фотографию с товаром, я распознаю штрихкод и номер заказа.",
        reply_markup=scan_keyboard
    )