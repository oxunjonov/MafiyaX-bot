import os
from dotenv import load_dotenv

load_dotenv()

# Bot sozlamalari
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Ma'lumotlar bazasi
DB_NAME = "mafiya_x.db"

# O'yin sozlamalari
MIN_PLAYERS = 4
MAX_PLAYERS = 50
DEFAULT_LANGUAGE = "uz"

# Vaqt sozlamalari (soniyalarda)
NIGHT_TIME = 60  # 1 daqiqa
DAY_TIME = 120  # 2 daqiqa
VOTE_TIME = 90  # 1.5 daqiqa
LAST_WORD_TIME = 30  # 30 soniya

# Qo'llab-quvvatlanadigan tillar
SUPPORTED_LANGUAGES = {
    "uz": "🇺🇿 O'zbek",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "tr": "🇹🇷 Türkçe",
    "fa": "🇮🇷 فارسی",
    "az": "🇦🇿 Azərbaycan"
}

# Emoji va belgilar
EMOJI = {
    "game": "🎮",
    "mafia": "🤵",
    "citizen": "👨",
    "komissar": "🕵️",
    "doctor": "👨‍⚕️",
    "killer": "🔪",
    "night": "🌙",
    "day": "☀️",
    "vote": "🗳",
    "diamond": "💎",
    "dollar": "💵",
    "shield": "🛡",
    "gun": "🔫"
}
