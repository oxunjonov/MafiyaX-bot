from functools import wraps
from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from typing import Union
from database.db import db
from utils.language import get_language_module, get_user_language, get_group_language

# Admin cache - tez ishlash uchun
admin_cache = {}

async def is_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
    """
    Foydalanuvchi admin ekanligini tekshirish
    Cache bilan - tez ishlash uchun
    """
    cache_key = f"{chat_id}_{user_id}"
    
    # Cache dan tekshirish
    if cache_key in admin_cache:
        return admin_cache[cache_key]
    
    try:
        chat_member = await bot.get_chat_member(chat_id, user_id)
        is_admin_status = chat_member.status in ["creator", "administrator"]
        
        # Cache ga saqlash (5 daqiqaga)
        admin_cache[cache_key] = is_admin_status
        return is_admin_status
    except:
        return False

async def is_group_chat(message: Union[Message, CallbackQuery]) -> bool:
    """Guruh chat ekanligini tekshirish"""
    if isinstance(message, CallbackQuery):
        message = message.message
    return message.chat.type in ["group", "supergroup"]

async def is_private_chat(message: Union[Message, CallbackQuery]) -> bool:
    """Shaxsiy chat ekanligini tekshirish"""
    if isinstance(message, CallbackQuery):
        message = message.message
    return message.chat.type == "private"

def group_only():
    """Decorator - faqat guruhlarda ishlaydi"""
    def decorator(func):
        @wraps(func)
        async def wrapper(message: Union[Message, CallbackQuery], *args, **kwargs):
            if not await is_group_chat(message):
                # Shaxsiy chatda xabar
                user_id = message.from_user.id
                language = await get_user_language(db, user_id)
                lang_data = get_language_module(language)
                
                if isinstance(message, CallbackQuery):
                    await message.answer(lang_data.ERROR_GROUP_ONLY, show_alert=True)
                else:
                    await message.answer(lang_data.ERROR_GROUP_ONLY)
                return
            
            return await func(message, *args, **kwargs)
        return wrapper
    return decorator

def private_only():
    """Decorator - faqat shaxsiy chatda ishlaydi"""
    def decorator(func):
        @wraps(func)
        async def wrapper(message: Union[Message, CallbackQuery], *args, **kwargs):
            if not await is_private_chat(message):
                # Guruhda xabar
                if isinstance(message, CallbackQuery):
                    await message.answer("⚠️ Bu buyruq faqat botda ishlaydi!", show_alert=True)
                else:
                    await message.answer("⚠️ Bu buyruq faqat botda ishlaydi! @MafiyaXBot ga o'ting.")
                return
            
            return await func(message, *args, **kwargs)
        return wrapper
    return decorator

def admin_only():
    """Decorator - faqat adminlar uchun"""
    def decorator(func):
        @wraps(func)
        async def wrapper(message: Union[Message, CallbackQuery], bot: Bot, *args, **kwargs):
            msg = message.message if isinstance(message, CallbackQuery) else message
            
            if not await is_admin(bot, msg.chat.id, message.from_user.id):
                # Admin emas
                language = await get_group_language(db, msg.chat.id)
                lang_data = get_language_module(language)
                
                if isinstance(message, CallbackQuery):
                    await message.answer(lang_data.ERROR_ADMIN_ONLY, show_alert=True)
                else:
                    await message.answer(lang_data.ERROR_ADMIN_ONLY)
                return
            
            return await func(message, bot, *args, **kwargs)
        return wrapper
    return decorator

def clear_admin_cache():
    """Admin cache ni tozalash"""
    global admin_cache
    admin_cache.clear()
