from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from src.handlers.commands import ScanState

router = Router()

@router.callback_query(F.data == "scan")
async def callback_scan(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ScanState.waiting_for_photo)
    await callback.message.answer("Отправь фотографию для сканирования.")
    await callback.answer()