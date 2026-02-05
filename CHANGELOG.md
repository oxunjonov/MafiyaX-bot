# 🔥 MAFIYA X - CHANGELOG

## v2.0 (2026-02-05) - PROFESSIONAL UPDATE 🚀

### ✨ Yangi Funksiyalar

#### 🎮 O'yin Tizimi
- ✅ **Smart Registration System**
  - 5 daqiqalik ro'yxatdan o'tish timer
  - Real-time progress bar
  - Avtomatik countdown notifications
  - Minimum/maksimum o'yinchilar kontroli

- ✅ **Advanced Timer System**
  - Har 10 soniyada avtomatik yangilanish
  - Countdown xabarlari (5 min, 3 min, 1 min, 30 sek, 10 sek)
  - Pause/Resume funksiyasi
  - Progress visualization

- ✅ **Role Assignment Without /start**
  - Bot start bosmagan bo'lsa ham rol xabari keladi!
  - Shaxsiy xabarlar orqali xavfsiz
  - Har bir o'yinchiga to'liq ma'lumot
  - Rol icon, jamoa, vazifa

#### 🔐 Huquqlar va Xavfsizlik
- ✅ **Smart Permission System**
  - Creator (o'yin yaratuvchisi) huquqlari
  - Admin huquqlari
  - Decorator pattern (@group_only, @admin_only, @private_only)
  - Admin cache (tez ishlash uchun)

- ✅ **Buyruqlar Ajratish**
  - Guruh buyruqlari faqat guruhda
  - Shaxsiy buyruqlar faqat botda
  - Xato xabarlari yo'naltirish bilan

- ✅ **Anti-Spam Protection**
  - Command cooldown
  - Flood prevention
  - Rate limiting

#### 🧹 Message Management
- ✅ **Auto Cleanup System**
  - O'yin xabarlarini tracking
  - O'yin tugagach avtomatik tozalash
  - Keep last N messages
  - Batch deletion

#### 🎯 Game Manager
- ✅ **Professional Game State**
  - Dataclass-based models
  - Player management
  - Team balance algorithm
  - Win condition checker
  - Real-time statistics

#### 📊 Sozlamalar
- ✅ **Config yangilandi**
  - Registration time: 300 sek (5 min)
  - Role emoji dictionary
  - Kengaytirilgan EMOJI set
  - Anti-spam sozlamalari

### 🔧 Texnik Yangilanishlar

#### 📁 Yangi Fayllar
```
utils/
├── permissions.py    # Permission system
├── game_manager.py   # Game state management  
├── timer.py         # Smart timer system
└── cleaner.py       # Message cleanup
```

#### 🏗️ Arxitektura
- **Separation of Concerns** - Har bir modul o'z vazifasi
- **Async/Await** - To'liq async kod
- **Type Hints** - Dataclasses va typing
- **Error Handling** - Try/except blocks
- **Caching** - Admin permissions cache

### 🐛 Tuzatilgan Xatolar

- ✅ Runtime.txt o'chirildi (Docker ishlatiladi)
- ✅ Import errors tuzatildi
- ✅ Permission checks optimized
- ✅ Message editing errors handled
- ✅ Timer race conditions fixed

### 📝 O'zgarishlar

#### Buyruqlar
- `/game` - Faqat guruhda, creator yoki admin
- `/stop` - O'yinni to'xtatish (creator yoki admin)
- Shaxsiy buyruqlar botda ishlaydi

#### O'yin Jarayoni
1. **Registration (5 min)**
   - Qo'shilish/Chiqish
   - Progress bar
   - Auto-start yoki manual start

2. **Starting (5 sek countdown)**
   - Rollar tarqatilmoqda
   - Animated countdown
   
3. **Role Notification**
   - Har bir o'yinchiga shaxsiy xabar
   - Bot start shart emas!
   - To'liq rol ma'lumoti

4. **Game (Keyingi versiyada)**
   - Tun/Kun sikli
   - Ovoz berish
   - G'alaba

### 🎯 Keyingi Versiyalar (v2.1+)

#### Rejalashtirilgan
- ⏳ To'liq tun/kun mexanikasi
- ⏳ Ovoz berish tizimi
- ⏳ 30+ rollar
- ⏳ 6 ta o'yin rejimi
- ⏳ Giveaway system
- ⏳ Shop va Achievements
- ⏳ Advanced statistics
- ⏳ Tournament mode

### 📦 O'rnatish

**GitHub dan yangilash:**
```bash
git pull origin main
```

**Yoki ZIP yuklab olish:**
- `mafiya-x-bot-v2.0.zip` ni yuklab oling
- Barcha fayllarni almashtiring
- Railway avtomatik deploy qiladi

### ⚠️ Muhim

- `.env` faylidagi `ADMIN_ID` majburiy!
- `BOT_TOKEN` to'g'ri kiritilganligini tekshiring
- Dockerfile orqali deploy qilish tavsiya etiladi

---

**Versiya:** 2.0  
**Sana:** 2026-02-05  
**Yaratuvchi:** oxunjonov
