import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database.db import db
from handlers import start, game

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Asosiy funksiya"""
    # Bot va Dispatcher yaratish
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    dp = Dispatcher()
    
    # Ma'lumotlar bazasini yaratish
    logger.info("Ma'lumotlar bazasi yaratilmoqda...")
    await db.create_tables()
    logger.info("Ma'lumotlar bazasi tayyor!")
    
    # Handlerlarni qo'shish
    dp.include_router(start.router)
    dp.include_router(game.router)
    
    # Botni ishga tushirish
    logger.info("Bot ishga tushmoqda...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot to'xtatildi!")
        
