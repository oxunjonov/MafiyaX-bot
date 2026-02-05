import aiosqlite
from config import DB_NAME

class Database:
    def __init__(self):
        self.db_name = DB_NAME
        
    async def create_tables(self):
        """Ma'lumotlar bazasi jadvallarini yaratish"""
        async with aiosqlite.connect(self.db_name) as db:
            # Foydalanuvchilar jadvali
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    language TEXT DEFAULT 'uz',
                    balance INTEGER DEFAULT 0,
                    diamonds INTEGER DEFAULT 0,
                    games_played INTEGER DEFAULT 0,
                    games_won INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Guruhlar jadvali
            await db.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    group_id INTEGER PRIMARY KEY,
                    group_name TEXT,
                    language TEXT DEFAULT 'uz',
                    game_mode TEXT DEFAULT 'classic',
                    night_time INTEGER DEFAULT 60,
                    day_time INTEGER DEFAULT 120,
                    vote_time INTEGER DEFAULT 90,
                    max_players INTEGER DEFAULT 50,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # O'yinlar jadvali
            await db.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER,
                    status TEXT DEFAULT 'waiting',
                    mode TEXT DEFAULT 'classic',
                    started_at TIMESTAMP,
                    finished_at TIMESTAMP,
                    winner TEXT,
                    FOREIGN KEY (group_id) REFERENCES groups(group_id)
                )
            """)
            
            # O'yinchi rollar jadvali
            await db.execute("""
                CREATE TABLE IF NOT EXISTS game_players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id INTEGER,
                    user_id INTEGER,
                    role TEXT,
                    team TEXT,
                    is_alive BOOLEAN DEFAULT 1,
                    FOREIGN KEY (game_id) REFERENCES games(game_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            
            # Qurollar jadvali
            await db.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    item_type TEXT,
                    quantity INTEGER DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            
            await db.commit()
    
    async def get_user(self, user_id: int):
        """Foydalanuvchi ma'lumotlarini olish"""
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                return await cursor.fetchone()
    
    async def add_user(self, user_id: int, username: str, first_name: str, language: str = 'uz'):
        """Yangi foydalanuvchi qo'shish"""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                """INSERT OR IGNORE INTO users 
                   (user_id, username, first_name, language) 
                   VALUES (?, ?, ?, ?)""",
                (user_id, username, first_name, language)
            )
            await db.commit()
    
    async def update_language(self, user_id: int, language: str):
        """Foydalanuvchi tilini yangilash"""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "UPDATE users SET language = ? WHERE user_id = ?",
                (language, user_id)
            )
            await db.commit()
    
    async def get_group(self, group_id: int):
        """Guruh ma'lumotlarini olish"""
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM groups WHERE group_id = ?", (group_id,)
            ) as cursor:
                return await cursor.fetchone()
    
    async def add_group(self, group_id: int, group_name: str):
        """Yangi guruh qo'shish"""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "INSERT OR IGNORE INTO groups (group_id, group_name) VALUES (?, ?)",
                (group_id, group_name)
            )
            await db.commit()
    
    async def update_balance(self, user_id: int, amount: int):
        """Foydalanuvchi balansini yangilash"""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id = ?",
                (amount, user_id)
            )
            await db.commit()
    
    async def update_diamonds(self, user_id: int, amount: int):
        """Foydalanuvchi olmoslarini yangilash"""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "UPDATE users SET diamonds = diamonds + ? WHERE user_id = ?",
                (amount, user_id)
            )
            await db.commit()
    
    async def get_top_players(self, limit: int = 10):
        """Top o'yinchilar ro'yxati"""
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                """SELECT user_id, username, first_name, games_won, games_played 
                   FROM users 
                   ORDER BY games_won DESC 
                   LIMIT ?""",
                (limit,)
            ) as cursor:
                return await cursor.fetchall()

# Database singleton
db = Database()
