import importlib
from config import DEFAULT_LANGUAGE

def get_language_module(language: str = DEFAULT_LANGUAGE):
    """Til modulini yuklash"""
    try:
        lang_module = importlib.import_module(f'languages.{language}')
        return lang_module
    except ImportError:
        # Agar til topilmasa, standart tilni qaytarish
        return importlib.import_module(f'languages.{DEFAULT_LANGUAGE}')

async def get_user_language(db, user_id: int) -> str:
    """Foydalanuvchi tilini olish"""
    user = await db.get_user(user_id)
    if user:
        return user['language']
    return DEFAULT_LANGUAGE

async def get_group_language(db, group_id: int) -> str:
    """Guruh tilini olish"""
    group = await db.get_group(group_id)
    if group:
        return group['language']
    return DEFAULT_LANGUAGE
  
