# PROFESSIONAL MULTI-LANGUAGE SYSTEM
# 8 tillar - Uzbek, Russian, English, Turkish, Kazakh, Tajik, Azerbaijani, Arabic

from typing import Dict

class LanguageSystem:
    """Professional 8 tillik tizim"""
    
    # Tillar ro'yxati
    LANGUAGES = {
        "uz": "🇺🇿 O'zbek",
        "ru": "🇷🇺 Русский",
        "en": "🇬🇧 English",
        "tr": "🇹🇷 Türkçe",
        "kz": "🇰🇿 Қазақша",
        "tj": "🇹🇯 Тоҷикӣ",
        "az": "🇦🇿 Azərbaycan",
        "ar": "🇸🇦 العربية"
    }
    
    # Davlat kodi → til mapping (avtomatik aniqlash)
    COUNTRY_TO_LANG = {
        "UZ": "uz",  # O'zbekiston
        "RU": "ru",  # Rossiya
        "KZ": "kz",  # Qozog'iston
        "TJ": "tj",  # Tojikiston
        "AZ": "az",  # Ozarbayjon
        "TR": "tr",  # Turkiya
        "SA": "ar",  # Saudiya Arabistoni
        "AE": "ar",  # BAA
        "US": "en",  # AQSH
        "GB": "en",  # Britaniya
    }
    
    @staticmethod
    def get_language(lang_code: str = "uz") -> Dict:
        """Til ma'lumotlarini olish"""
        return TEXTS.get(lang_code, TEXTS["uz"])
    
    @staticmethod
    def detect_language_from_country(country_code: str) -> str:
        """Davlat kodi orqali tilni aniqlash"""
        return LanguageSystem.COUNTRY_TO_LANG.get(country_code, "uz")

# =====================================================
# BARCHA MATNLAR - 8 TIL
# =====================================================

TEXTS = {
    # O'ZBEK TILI
    "uz": {
        # Guruhga qo'shilish
        "first_message": """
🎭 **MAFIYA X BOT**

Assalomu alaykum! 👋

Men professional Mafiya o'yini botiman!

🎮 **Qanday o'ynash:**
1. Meni guruhga admin qiling
2. `/game` buyrug'i bilan o'yin boshlang
3. O'yinchilar qo'shiladi
4. O'yin avtomatik boshlanadi!

📋 **Buyruqlar:**
• `/game` - O'yin boshlash
• `/stop` - To'xtatish
• `/help` - Yordam
• `/lang` - Tilni o'zgartirish

Omad tilaymiz! 🍀
""",
        
        # Qo'shilish xabarlari
        "join_start_first": """
✅ **Botga xush kelibsiz!**

Iltimos, avval botni ishga tushiring:

👇 Quyidagi tugmani bosing:
""",
        
        "join_success": """
✅ **Siz o'yinga muvaffaqiyatli qo'shildingiz!**

Guruhga qaytib, o'yin boshlanishini kuting.

👇 Guruhga qaytish:
""",
        
        "btn_start_bot": "🤖 Botni ishga tushirish",
        "btn_return_to_group": "↩️ Guruhga qaytish",
        
        # O'yin xabarlari
        "game_started": "✅ O'yin boshlandi!",
        "night_started": "🌙 TUN {day} BOSHLANDI",
        "day_started": "☀️ KUN {day} BOSHLANDI",
        
        # Rollar
        "your_role": """
🎭 **SIZNING ROLINGIZ**

{emoji} **{role_name}**

{team_info}

📝 **Tavsif:**
{description}

Omad! 🍀
""",
        
        "team_mafia": "🔴 **Jamoa:** Mafiya",
        "team_citizen": "🟢 **Jamoa:** Tinch aholi",
        "team_neutral": "🟡 **Jamoa:** Neytral",
        
        # Ovoz berish
        "voting_started": "🗳️ **OVOZ BERISH BOSHLANDI!**\n\n⏰ Vaqt: {time} soniya",
        "voting_result": "🪢 **OSILDI:** {player}",
        
        # AFK
        "afk_warning": "⚠️ Siz 1 fazada faol bo'lmadingiz!\n\nYana faolsiz bo'lsangiz, chiqarilasiz!",
        "afk_removed": "⛔ Siz faol emasligingiz sababli o'yindan chiqarildingiz",
        
        # Almaz
        "almaz_balance": "💎 **Almaz:** {balance}",
        "almaz_insufficient": "❌ Yetarli almaz yo'q!",
        "almaz_purchase_success": "✅ Xarid muvaffaqiyatli!",
    },
    
    # РУССКИЙ ЯЗЫК
    "ru": {
        "first_message": """
🎭 **МАФИЯ X БОТ**

Здравствуйте! 👋

Я профессиональный бот для игры в Мафию!

🎮 **Как играть:**
1. Сделайте меня админом группы
2. Начните игру командой `/game`
3. Игроки присоединяются
4. Игра начинается автоматически!

📋 **Команды:**
• `/game` - Начать игру
• `/stop` - Остановить
• `/help` - Помощь
• `/lang` - Изменить язык

Удачи! 🍀
""",
        
        "join_success": "✅ **Вы успешно присоединились к игре!**\n\nВернитесь в группу и ждите начала.\n\n👇 Вернуться в группу:",
        "btn_start_bot": "🤖 Запустить бота",
        "btn_return_to_group": "↩️ Вернуться в группу",
        "game_started": "✅ Игра началась!",
        "afk_removed": "⛔ Вы были удалены из игры за неактивность",
    },
    
    # ENGLISH
    "en": {
        "first_message": """
🎭 **MAFIA X BOT**

Hello! 👋

I'm a professional Mafia game bot!

🎮 **How to play:**
1. Make me group admin
2. Start game with `/game`
3. Players join
4. Game starts automatically!

📋 **Commands:**
• `/game` - Start game
• `/stop` - Stop
• `/help` - Help
• `/lang` - Change language

Good luck! 🍀
""",
        
        "join_success": "✅ **You successfully joined the game!**\n\nReturn to group and wait.\n\n👇 Return to group:",
        "btn_start_bot": "🤖 Start bot",
        "btn_return_to_group": "↩️ Return to group",
        "game_started": "✅ Game started!",
        "afk_removed": "⛔ You were removed for inactivity",
    },
    
    # TÜRKÇE
    "tr": {
        "first_message": """
🎭 **MAFYA X BOT**

Merhaba! 👋

Ben profesyonel Mafya oyunu botuyum!

🎮 **Nasıl oynanır:**
1. Beni grup yöneticisi yapın
2. `/game` komutu ile oyunu başlatın
3. Oyuncular katılır
4. Oyun otomatik başlar!

📋 **Komutlar:**
• `/game` - Oyun başlat
• `/stop` - Durdur
• `/help` - Yardım
• `/lang` - Dil değiştir

İyi şanslar! 🍀
""",
        
        "join_success": "✅ **Oyuna başarıyla katıldınız!**\n\nGruba dönün ve bekleyin.\n\n👇 Gruba dön:",
        "btn_start_bot": "🤖 Botu başlat",
        "btn_return_to_group": "↩️ Gruba dön",
        "game_started": "✅ Oyun başladı!",
        "afk_removed": "⛔ Hareketsizlik nedeniyle çıkarıldınız",
    },
    
    # ҚАЗАҚША
    "kz": {
        "first_message": """
🎭 **МАФИЯ X БОТ**

Сәлеметсіз бе! 👋

Мен кәсіби Мафия ойын ботымын!

🎮 **Қалай ойнау:**
1. Мені топ әкімшісі етіңіз
2. `/game` командасымен ойынды бастаңыз
3. Ойыншылар қосылады
4. Ойын автоматты басталады!

📋 **Командалар:**
• `/game` - Ойын бастау
• `/stop` - Тоқтату
• `/help` - Көмек
• `/lang` - Тілді өзгерту

Сәттілік! 🍀
""",
        
        "join_success": "✅ **Сіз ойынға сәтті қосылдыңыз!**\n\nТопқа оралып, күтіңіз.\n\n👇 Топқа орал:",
        "btn_start_bot": "🤖 Ботты бастау",
        "btn_return_to_group": "↩️ Топқа орал",
    },
    
    # ТОҶИКӢ
    "tj": {
        "first_message": """
🎭 **МАФИЯ X БОТ**

Салом! 👋

Ман боти касбии бозии Мафия ҳастам!

🎮 **Чӣ тавр бозӣ кунем:**
1. Маро админ кунед
2. Бозиро бо `/game` оғоз кунед
3. Бозингарон ҳамроҳ мешаванд
4. Бозӣ худкор оғоз мешавад!

📋 **Фармонҳо:**
• `/game` - Оғози бозӣ
• `/stop` - Қатъ кардан
• `/help` - Кӯмак
• `/lang` - Тағйири забон

Муваффақ бошед! 🍀
""",
        
        "join_success": "✅ **Шумо бо муваффақият ба бозӣ ҳамроҳ шудед!**",
        "btn_start_bot": "🤖 Ботро оғоз кунед",
    },
    
    # AZƏRBAYCAN
    "az": {
        "first_message": """
🎭 **MAFIYA X BOT**

Salam! 👋

Mən peşəkar Mafiya oyun botuyam!

🎮 **Necə oynamaq:**
1. Məni qrup admini edin
2. `/game` əmri ilə oyunu başladın
3. Oyunçular qoşulur
4. Oyun avtomatik başlayır!

📋 **Əmrlər:**
• `/game` - Oyun başlat
• `/stop` - Dayandır
• `/help` - Kömək
• `/lang` - Dili dəyiş

Uğurlar! 🍀
""",
        
        "join_success": "✅ **Oyuna uğurla qoşuldunuz!**\n\nQrupa qayıdın və gözləyin.\n\n👇 Qrupa qayıt:",
        "btn_start_bot": "🤖 Botu başlat",
    },
    
    # العربية
    "ar": {
        "first_message": """
🎭 **مافيا X بوت**

مرحبا! 👋

أنا بوت محترف للعبة المافيا!

🎮 **كيفية اللعب:**
1. اجعلني مسؤول المجموعة
2. ابدأ اللعبة بأمر `/game`
3. ينضم اللاعبون
4. تبدأ اللعبة تلقائياً!

📋 **الأوامر:**
• `/game` - بدء اللعبة
• `/stop` - إيقاف
• `/help` - مساعدة
• `/lang` - تغيير اللغة

حظاً موفقاً! 🍀
""",
        
        "join_success": "✅ **لقد انضممت إلى اللعبة بنجاح!**\n\nارجع إلى المجموعة وانتظر.\n\n👇 العودة للمجموعة:",
        "btn_start_bot": "🤖 تشغيل البوت",
        "btn_return_to_group": "↩️ العودة للمجموعة",
    },
}

def get_text(key: str, lang: str = "uz", **kwargs) -> str:
    """
    Matnni olish va format qilish
    
    Args:
        key: Matn kaliti
        lang: Til kodi
        **kwargs: Format parametrlari
    
    Returns:
        Formatlangan matn
    """
    lang_texts = TEXTS.get(lang, TEXTS["uz"])
    text = lang_texts.get(key, TEXTS["uz"].get(key, ""))
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except:
            return text
    
    return text
