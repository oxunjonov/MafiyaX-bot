from functools import wraps
from aiogram.types import Message
from aiogram import Bot

def delete_command():
    """
    Decorator - guruh buyruqlarini avtomatik o'chirish
    Bot admin bo'lishi kerak!
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(message: Message, bot: Bot = None, *args, **kwargs):
            # Guruhda bo'lsa va bot parameter bo'lsa
            if message.chat.type in ["group", "supergroup"]:
                # Buyruq xabarini o'chirish
                try:
                    if bot:
                        await bot.delete_message(message.chat.id, message.message_id)
                    else:
                        # Agar bot parameter yo'q bo'lsa, message.bot dan olish
                        await message.bot.delete_message(message.chat.id, message.message_id)
                except Exception as e:
                    # Bot admin emas yoki ruxsat yo'q
                    pass
            
            return await func(message, bot, *args, **kwargs) if bot else await func(message, *args, **kwargs)
        return wrapper
    return decorator
