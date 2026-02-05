from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SUPPORTED_LANGUAGES

def get_main_menu(lang_data):
    """Asosiy menyu klaviaturasi"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=lang_data.BTN_START_GAME,
                callback_data="start_game"
            )
        ],
        [
            InlineKeyboardButton(
                text=lang_data.BTN_RULES,
                callback_data="rules"
            ),
            InlineKeyboardButton(
                text=lang_data.BTN_HELP,
                callback_data="help"
            )
        ],
        [
            InlineKeyboardButton(
                text=lang_data.BTN_PROFILE,
                callback_data="profile"
            ),
            InlineKeyboardButton(
                text=lang_data.BTN_TOP,
                callback_data="top"
            )
        ],
        [
            InlineKeyboardButton(
                text=lang_data.BTN_LANGUAGE,
                callback_data="change_language"
            )
        ]
    ])
    return keyboard

def get_language_keyboard():
    """Til tanlash klaviaturasi"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🇺🇿 O'zbek",
                callback_data="lang_uz"
            ),
            InlineKeyboardButton(
                text="🇷🇺 Русский",
                callback_data="lang_ru"
            )
        ],
        [
            InlineKeyboardButton(
                text="🇬🇧 English",
                callback_data="lang_en"
            ),
            InlineKeyboardButton(
                text="🇹🇷 Türkçe",
                callback_data="lang_tr"
            )
        ],
        [
            InlineKeyboardButton(
                text="🇮🇷 فارسی",
                callback_data="lang_fa"
            ),
            InlineKeyboardButton(
                text="🇦🇿 Azərbaycan",
                callback_data="lang_az"
            )
        ]
    ])
    return keyboard

def get_game_join_keyboard(lang_data):
    """O'yinga qo'shilish klaviaturasi"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Qo'shilish / Join",
                callback_data="join_game"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Chiqish / Leave",
                callback_data="leave_game"
            )
        ],
        [
            InlineKeyboardButton(
                text="🎮 Boshlash / Start",
                callback_data="start_game_now"
            )
        ]
    ])
    return keyboard

def get_game_modes_keyboard():
    """O'yin modlarini tanlash klaviaturasi"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Classic", callback_data="mode_classic"),
            InlineKeyboardButton(text="Super", callback_data="mode_super")
        ],
        [
            InlineKeyboardButton(text="Mega", callback_data="mode_mega"),
            InlineKeyboardButton(text="Real", callback_data="mode_real")
        ],
        [
            InlineKeyboardButton(text="Zombie", callback_data="mode_zombie"),
            InlineKeyboardButton(text="Para", callback_data="mode_para")
        ]
    ])
    return keyboard

def get_settings_keyboard(lang_data):
    """Sozlamalar klaviaturasi"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⏰ Vaqtlar / Time",
                callback_data="settings_time"
            )
        ],
        [
            InlineKeyboardButton(
                text="🎭 Rollar / Roles",
                callback_data="settings_roles"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔧 O'yin mode / Game Mode",
                callback_data="settings_mode"
            )
        ],
        [
            InlineKeyboardButton(
                text="🌍 Til / Language",
                callback_data="settings_language"
            )
        ],
        [
            InlineKeyboardButton(
                text="◀️ Orqaga / Back",
                callback_data="back_to_menu"
            )
        ]
    ])
    return keyboard

def get_back_button(lang_data):
    """Orqaga qaytish tugmasi"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="◀️ Orqaga / Back",
                callback_data="back_to_menu"
            )
        ]
    ])
    return keyboard
  
