# O'zbek tili (Lotin)

LANGUAGE_NAME = "🇺🇿 O'zbek"

# Asosiy matnlar
START_MESSAGE = """👋 Assalomu alaykum!

🎭 **MAFIYA X** botiga xush kelibsiz!

Bu bot orqali siz do'stlaringiz bilan qiziqarli Mafiya o'yinini o'ynashingiz mumkin.

📚 O'yin haqida to'liq ma'lumot olish uchun /help buyrug'ini yuboring.

🎮 O'yinni boshlash uchun guruhga qo'shing va /game buyrug'ini yuboring!
"""

HELP_MESSAGE = """📖 **MAFIYA X - Yordam**

🎮 **Asosiy buyruqlar:**
/start - Botni ishga tushirish
/help - Yordam
/game - O'yinni boshlash
/sozlamalar - Guruh sozlamalari
/profile - Profilingiz
/top - Reyting

🌍 **Tilni o'zgartirish:**
/language - Til tanlash

📊 **Statistika:**
/stats - O'yin statistikasi
/balance - Balansingiz

💎 **Giveaway:**
/send - Olmoslarni tarqatish
/change - O'yin o'tkazish
/ghimoya - Himoya tarqatish

📝 **Qo'shimcha:**
Botni guruhga qo'shib, admin qiling va /game buyrug'i bilan o'yinni boshlang!

O'yin haqida batafsil ma'lumot: /rules
"""

RULES_MESSAGE = """📜 **O'YIN QOIDALARI**

🎭 **Mafiya** - bu strategik guruh o'yini.

**Maqsad:**
🟢 Tinch aholi - mafiyalarni topish va osish
🔴 Mafiya - tinch aholini yo'q qilish
🟡 Yakka rollar - o'z maqsadiga erishish

**O'yin jarayoni:**
🌙 Tun - rollar o'z vazifalarini bajaradi
☀️ Kun - muhokama va ovoz berish

**Asosiy rollar:**
🤵 Don - Mafiya sardori
🕵️ Komissar - Mafiyani qidiradigan detektiv
👨 Tinch aholi - oddiy fuqaro
🔪 Qotil - mustaqil o'yinchi

To'liq qo'llanma: @MafiyaXGuide
"""

# Tugmalar
BTN_START_GAME = "🎮 O'yinni boshlash"
BTN_RULES = "📜 Qoidalar"
BTN_HELP = "❓ Yordam"
BTN_LANGUAGE = "🌍 Til"
BTN_PROFILE = "👤 Profil"
BTN_TOP = "🏆 Top"
BTN_SETTINGS = "⚙️ Sozlamalar"

# Til tanlash
SELECT_LANGUAGE = "🌍 Tilni tanlang:"
LANGUAGE_CHANGED = "✅ Til muvaffaqiyatli o'zgartirildi!"

# O'yin matnlari
GAME_STARTING = "🎮 O'yin boshlanmoqda..."
GAME_STARTED = "✅ O'yin boshlandi!"
NOT_ENOUGH_PLAYERS = "❌ Kamida 4 ta o'yinchi kerak!"
GAME_ALREADY_RUNNING = "⚠️ O'yin allaqachon boshlanган!"
JOINED_GAME = "✅ O'yinga qo'shildi: {name}"
LEFT_GAME = "❌ O'yindan chiqdi: {name}"

# Rollar
ROLE_ASSIGNED = "🎭 Sizning rolingiz: {role}"
ROLE_DON = "🤵 Don"
ROLE_MAFIA = "🤵‍♂️ Mafiya"
ROLE_KOMISSAR = "🕵️ Komissar Katani"
ROLE_CITIZEN = "👨 Tinch aholi"
ROLE_DOCTOR = "👨‍⚕️ Doktor"
ROLE_KILLER = "🔪 Qotil"

# Xatolar
ERROR_GROUP_ONLY = "❌ Bu buyruq faqat guruhlarda ishlaydi!"
ERROR_ADMIN_ONLY = "❌ Bu buyruq faqat adminlar uchun!"
ERROR_GAME_CREATOR_ONLY = "❌ Bu buyruq faqat o'yin yaratuvchisi yoki adminlar uchun!"
ERROR_OCCURRED = "❌ Xatolik yuz berdi. Qaytadan urinib ko'ring."
ERROR_PRIVATE_ONLY = "⚠️ Bu buyruq faqat botda ishlaydi! @MafiyaXBot ga o'ting."
ERROR_GAME_EXISTS = "⚠️ Bu guruhda allaqachon o'yin mavjud!"
ERROR_NO_GAME = "❌ Hozir o'yin yo'q!"
ERROR_ALREADY_JOINED = "⚠️ Siz allaqachon o'yinda qatnashyapsiz!"
ERROR_GAME_FULL = "❌ O'yin to'lgan! Maksimum {max} ta o'yinchi."
ERROR_GAME_STARTED = "❌ O'yin allaqachon boshlangan!"
ERROR_NOT_ENOUGH_PLAYERS = "❌ Kamida {min} ta o'yinchi kerak!"

# Muvaffaqiyatli
SUCCESS = "✅ Muvaffaqiyatli!"
SUCCESS_JOINED = "✅ O'yinga qo'shildingiz!"
SUCCESS_LEFT = "❌ O'yindan chiqdingiz!"

# Registration (Ro'yxatdan o'tish)
REGISTRATION_STARTED = """
🎮 **MAFIYA X - Yangi O'yin**

O'yinga ro'yxatdan o'tish boshlandi!

👥 **O'yinchilar:** {current}/{max}
⏰ **Vaqt:** {time} qoldi
📊 **Minimum:** {min} ta o'yinchi

{progress_bar}

**O'yinchilar ro'yxati:**
{players_list}
"""

REGISTRATION_UPDATE = """
🎮 **MAFIYA X - O'yin ro'yxati**

👥 **O'yinchilar:** {current}/{max}
⏰ **Vaqt:** {time} qoldi

{progress_bar}

**Ro'yxat:**
{players_list}
"""

REGISTRATION_ENDING = "⏰ **{time} soniya qoldi!** Tezroq qo'shiling! 🚨"
REGISTRATION_CLOSED = "🔒 Ro'yxatdan o'tish yopildi! O'yin boshlanmoqda..."

# O'yin boshlanishi
GAME_STARTING_COUNTDOWN = """
🎮 **O'YIN BOSHLANMOQDA!**

⏰ **{seconds} soniyada** boshlanadi...

👥 Ishtirokchilar: **{count} ta**
🎭 Rollar tarqatilmoqda...

{progress_bar}
"""

ROLE_NOTIFICATION = """
🎭 **SIZNING ROLINGIZ**

{role_icon} **{role_name}**

{role_description}

{team_info}

🎯 **Vazifangiz:** {role_task}

Omad tilaymiz! 🍀
"""

# Jamoa ma'lumotlari
TEAM_MAFIA = "🔴 **Jamoa:** Mafiya"
TEAM_CITIZEN = "🟢 **Jamoa:** Tinch aholi"
TEAM_INDEPENDENT = "🟡 **Jamoa:** Mustaqil"

# Rol vazifalar
TASK_DON = "Tunda kimni o'ldirishni hal qiling va mafiyani boshqaring"
TASK_MAFIA = "Donga bo'ysunib, tinch aholini yo'q qiling"
TASK_KOMISSAR = "Tunda kimnidir tekshiring va mafiyani toping"
TASK_CITIZEN = "Kunduzgi muhokamada mafiyani toping va osing"
TASK_DOCTOR = "Tunda kimnidir himoya qiling va hayot qutqaring"

# Tun/Kun
NIGHT_STARTED = """
🌙 **TUN {day} BOSHLANDI**

Shahar uxlayapti...
Rollar o'z vazifalarini bajarishmoqda.

⏰ Vaqt: **{time}**
"""

DAY_STARTED = """
☀️ **KUN {day} BOSHLANDI**

Shahar uyg'ondi!

{deaths_text}

⏰ Muhokama vaqti: **{time}**
"""

VOTING_STARTED = """
🗳️ **OVOZ BERISH BOSHLANDI**

Kimni osmoqchisiz?

⏰ Vaqt: **{time}**

**Nomzodlar:**
{candidates}
"""

# O'lim xabarlari
DEATH_MAFIA_KILL = "🔪 **{name}** ({role}) tun payti o'ldirildi..."
DEATH_HANGED = "🪢 **{name}** ({role}) aholining qaroriga ko'ra osildi..."
DEATH_MULTIPLE = "💀 **Bu tunda {count} ta odam halok bo'ldi!**"
NO_DEATHS = "✨ **Bu tunda hech kim o'lmadi!**"

# G'alaba
VICTORY_CITIZEN = """
🎉 **TINCH AHOLI G'ALABA QOZONDI!**

Barcha mafiyalar topildi va adalat g'alaba qildi!

🏆 **G'oliblar:**
{winners}

📊 **Statistika:**
{stats}
"""

VICTORY_MAFIA = """
😈 **MAFIYA G'ALABA QOZONDI!**

Shahar mafiya qo'lida!

🏆 **G'oliblar:**
{winners}

📊 **Statistika:**
{stats}
"""

# Sozlamalar
SETTINGS_MAIN = """
⚙️ **GURUH SOZLAMALARI**

🌍 **Til:** {language}
🎮 **O'yin rejimi:** {mode}
👥 **O'yinchilar:** {min}-{max}

⏰ **Vaqtlar:**
• Ro'yxat: {reg_time}
• Tun: {night_time}
• Kun: {day_time}
• Ovoz: {vote_time}
"""

SETTINGS_TIME = "⏰ **Vaqt sozlamalari**\n\nQaysi vaqtni o'zgartirmoqchisiz?"
SETTINGS_ROLES = "🎭 **Rollar sozlamalari**\n\nQaysi rollarni yoqish/o'chirish?"
SETTINGS_MODE = "🎮 **O'yin rejimini tanlang**"

# Statistika
STATS_PERSONAL = """
📊 **SHAXSIY STATISTIKA**

🎮 **O'yinlar:** {games}
🏆 **G'alabalar:** {wins}
📈 **Win Rate:** {winrate}%

🎭 **Sevimli rol:** {favorite_role}
💎 **Olmoslar:** {diamonds}
💵 **Dollar:** {balance}

⭐ **Achievements:** {achievements}/10
"""

STATS_GROUP = """
📊 **GURUH STATISTIKA**

🎮 **Jami o'yinlar:** {total_games}
👥 **Jami o'yinchilar:** {total_players}

🏆 **Top 5 O'yinchilar:**
{top_players}

📈 **Faol o'yinchilar:** {active_players}
"""
