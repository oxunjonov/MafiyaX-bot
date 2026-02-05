# 🎭 MAFIYA X - Telegram Bot

Telegram uchun ko'p tilli Mafiya o'yini boti.

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
- Odilbek - Bosh dasturchi
- Xusanov - G'oya muallifi
