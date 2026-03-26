from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from src.config import BOT_TOKEN

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Импортируем роутеры
from src.handlers import commands, photo, callback

dp.include_router(commands.router)
dp.include_router(photo.router)
dp.include_router(callback.router)