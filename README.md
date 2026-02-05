# 🎭 MAFIYA X v2.0 - Professional Telegram Bot

Telegram uchun ko'p tilli, professional Mafiya o'yini boti.

## ✨ Asosiy Xususiyatlar

### 🎮 O'yin Mexanikasi
- ✅ **Smart Registration System** - 5 daqiqalik timer bilan
- ✅ **Automatic Role Assignment** - Balanced algorithm
- ✅ **Role Notifications** - Bot start shart emas!
- ✅ **Clean Message System** - Avtomatik tozalash
- ✅ **Progress Bar** - Real-time updates
- ✅ **Countdown Timer** - Notification system bilan

### 🔐 Huquqlar va Xavfsizlik
- ✅ **Smart Permissions** - Creator va Admin control
- ✅ **Group/Private Separation** - Ajratilgan buyruqlar
- ✅ **Anti-Spam Protection** - Flood prevention
- ✅ **Admin Cache** - Tez ishlash

### 🌍 Ko'p Tilli Qo'llab-quvvatlash
- 🇺🇿 O'zbek (Lotin)
- 🇷🇺 Русский
- 🇬🇧 English
- 🇹🇷 Türkçe
- 🇮🇷 فارسی
- 🇦🇿 Azərbaycan

### 🎭 Rollar (Hozirda)
- 🤵 **Don** - Mafiya sardori
- 🤵‍♂️ **Mafiya** - Mafiya a'zosi
- 🕵️ **Komissar Katani** - Detektiv
- 👨 **Tinch Aholi** - Oddiy fuqaro
- 👨‍⚕️ **Doktor** - Shifokor (6+ o'yinchi)

## 🚀 O'rnatish

### 1. Repository ni klonlash
```bash
git clone https://github.com/oxunjonov/MafiyaX-bot.git
cd MafiyaX-bot
```

### 2. Virtual muhitni yaratish (ixtiyoriy)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. .env faylini sozlash
`.env` faylini yarating va quyidagilarni kiriting:
```
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_id
```

### 5. Botni ishga tushirish
```bash
python bot.py
```

## 🚀 Railway.app ga Deploy qilish

### 1. GitHub ga yuklash
```bash
git add .
git commit -m "Update to v2.0"
git push origin main
```

### 2. Railway.app da
1. [railway.app](https://railway.app) ga kiring
2. Loyihangizni oching yoki yangi yarating
3. "Deploy from GitHub repo" → **MafiyaX-bot**
4. **Environment Variables** qo'shing:
   - `BOT_TOKEN` = sizning bot tokeningiz
   - `ADMIN_ID` = sizning telegram ID

### 3. Deploy
Railway avtomatik deploy qiladi va bot 24/7 ishlaydi!

## 📋 Buyruqlar

### 👥 Guruh Buyruqlari (Faqat guruhlarda)
- `/game` - O'yin boshlash (Creator yoki Admin)
- `/stop` - O'yinni to'xtatish (Creator yoki Admin)
- `/sozlamalar` - Guruh sozlamalari (Admin)
- `/stats` - Guruh statistikasi
- `/rules` - O'yin qoidalari

### 🏠 Shaxsiy Buyruqlar (Faqat botda)
- `/start` - Botni ishga tushirish
- `/help` - Yordam
- `/profile` - Profilingiz
- `/language` - Tilni o'zgartirish
- `/balance` - Balansingiz

## 🎮 O'yin Jarayoni

### 1️⃣ Ro'yxatdan O'tish (5 daqiqa)
- `/game` buyrug'ini yuboring
- O'yinchilar "Qo'shilish" tugmasini bosadi
- Timer tugagach yoki admin "Boshlash" tugmasini bossa - o'yin boshlanadi

### 2️⃣ Rollar Tarqatiladi
- Har bir o'yinchiga **shaxsiy xabar** keladi
- **Bot start bosmagan bo'lsa ham** rol xabari keladi!
- Rol, jamoa va vazifa ko'rsatiladi

### 3️⃣ O'yin Boshlandi
- 🌙 **Tun** - Rollar o'z vazifalarini bajaradi
- ☀️ **Kun** - Muhokama va ovoz berish
- 🏆 **G'alaba** - Tinch aholi yoki Mafiya yutadi

## 🛠 Texnologiyalar

- **Python 3.11+**
- **aiogram 3.4.1** - Telegram Bot API
- **aiosqlite** - Async SQLite database
- **python-dotenv** - Environment variables
- **Docker** - Containerization

## 📊 Arxitektura

```
mafiya-x-bot/
├── bot.py                 # Asosiy fayl
├── config.py             # Sozlamalar
├── database/
│   └── db.py            # Ma'lumotlar bazasi
├── handlers/
│   ├── start.py         # Shaxsiy chat handlers
│   └── game.py          # Guruh o'yin handlers
├── keyboards/
│   └── inline.py        # Inline klaviaturalar
├── languages/
│   ├── uz.py           # O'zbek tili
│   ├── ru.py           # Rus tili
│   ├── en.py           # Ingliz tili
│   ├── tr.py           # Turk tili
│   ├── fa.py           # Fors tili
│   └── az.py           # Ozarbayjon tili
└── utils/
    ├── permissions.py   # Ruxsat tizimi
    ├── game_manager.py  # O'yin boshqaruvi
    ├── timer.py         # Timer tizimi
    ├── cleaner.py       # Xabar tozalash
    └── language.py      # Til funksiyalari
```

## 🔄 Keyingi Yangilanishlar (v2.1+)

- ⏳ 30+ rollar (Admiral, Koldun, Daydi, Qotil va h.k.)
- ⏳ 6 ta o'yin rejimi (Classic, Super, Mega, Real, Zombie, Para)
- ⏳ To'liq tun/kun mexanikasi
- ⏳ Ovoz berish tizimi
- ⏳ Giveaway tizimi
- ⏳ Olmos/Dollar tizimi
- ⏳ Shop (qurollar, himoya)
- ⏳ Achievement system
- ⏳ Advanced statistika

## 📞 Yordam

Savollar yoki muammolar bo'lsa:
- GitHub Issues: [Issues](https://github.com/oxunjonov/MafiyaX-bot/issues)
- Telegram: @oxunjonov

## 📄 Litsenziya

MIT License

---

**Versiya:** 2.0  
**Oxirgi yangilanish:** 2026-02-05  
**Yaratuvchi:** oxunjonov

## 🌍 Qo'llab-quvvatlanadigan Tillar

- 🇺🇿 O'zbek (Lotin)
- 🇷🇺 Русский
- 🇬🇧 English
- 🇹🇷 Türkçe
- 🇮🇷 فارسی
- 🇦🇿 Azərbaycan

## ⚙️ O'rnatish

### 1. Repository ni klonlash
```bash
git clone https://github.com/YOUR_USERNAME/mafiya-x-bot.git
cd mafiya-x-bot
```

### 2. Virtual muhitni yaratish (ixtiyoriy)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. .env faylini sozlash
`.env` faylini yarating va quyidagilarni kiriting:
```
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_id
```

### 5. Botni ishga tushirish
```bash
python bot.py
```

## 🚀 Railway.app ga Deploy qilish

### 1. GitHub ga yuklash
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/mafiya-x-bot.git
git push -u origin main
```

### 2. Railway.app da loyiha yaratish
1. [railway.app](https://railway.app) ga kiring
2. "New Project" → "Deploy from GitHub repo"
3. Repository ni tanlang
4. Environment Variables ga `.env` dan ma'lumotlarni kiriting:
   - `BOT_TOKEN` = sizning bot tokeningiz
   - `ADMIN_ID` = sizning telegram ID

### 3. Deploy
Railway avtomatik ravishda deploy qiladi va bot 24/7 ishlaydi!

## 📋 Asosiy Buyruqlar

- `/start` - Botni ishga tushirish
- `/help` - Yordam
- `/game` - O'yin boshlash (faqat guruhlarda)
- `/language` - Tilni o'zgartirish
- `/profile` - Profilingiz
- `/rules` - O'yin qoidalari

## 🎮 O'yin Xususiyatlari

### Hozirda Mavjud:
- ✅ 6 tilda ishlaydi
- ✅ Oddiy o'yin rejimi
- ✅ 4+ rol (Don, Komissar, Mafiya, Tinch aholi)
- ✅ Profil tizimi
- ✅ Ma'lumotlar bazasi

### Keyingi Yangilanishlar:
- ⏳ Barcha 30+ rollar
- ⏳ 6 ta o'yin rejimi (Classic, Super, Mega, Real, Zombie, Para)
- ⏳ Giveaway tizimi
- ⏳ Olmos/Dollar tizimi
- ⏳ To'liq o'yin mexanikasi
- ⏳ Admin panel

## 🛠 Texnologiyalar

- Python 3.10+
- aiogram 3.4.1
- aiosqlite
- python-dotenv

## 📞 Yordam

Savollar yoki muammolar bo'lsa:
- GitHub Issues: [Issues](https://github.com/YOUR_USERNAME/mafiya-x-bot/issues)
- Telegram: @YourUsername

## 📄 Litsenziya

MIT License

---

**Yaratuvchilar:**
- Abdusamigʻ - Bosh dasturchi

