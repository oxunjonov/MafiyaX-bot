#!/usr/bin/env python3
# MAFIYA X - PROFESSIONAL COMPLETE BOT

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from config import BOT_TOKEN
from database.db import db
from handlers import start, game

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    await db.create_tables()
    
    dp.include_router(start.router)
    dp.include_router(game.router)
    
    # Commands
    await bot.set_my_commands([
        BotCommand(command="start", description="Botni ishga tushirish"),
        BotCommand(command="help", description="Yordam"),
        BotCommand(command="profile", description="Profil"),
    ], scope=types.BotCommandScopeAllPrivateChats())
    
    await bot.set_my_commands([
        BotCommand(command="game", description="O'yin boshlash"),
        BotCommand(command="stop", description="To'xtatish"),
    ], scope=types.BotCommandScopeAllGroupChats())
    
    logger.info("🚀 Bot started!")
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
