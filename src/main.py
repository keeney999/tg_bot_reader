import asyncio
from src.bot import dp, bot
from src.utils.logger import logger

async def main():
    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())