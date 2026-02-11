from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from database.db import db
from utils.language import get_language_module, get_group_language
from keyboards.inline import get_game_join_keyboard, get_game_modes_keyboard
import asyncio
from typing import Dict, List

router = Router()

# Guruhlar uchun aktiv o'yinlar
active_games: Dict[int, dict] = {}

@router.message(Command("game"))
async def cmd_game(message: Message):
    """O'yin yaratish buyrug'i"""
    # Faqat guruhlarda ishlaydi
    if message.chat.type not in ["group", "supergroup"]:
        user_id = message.from_user.id
        language = await get_user_language(db, user_id)
        lang_data = get_language_module(language)
        await message.answer(lang_data.ERROR_GROUP_ONLY)
        return
    
    group_id = message.chat.id
    group_name = message.chat.title
    
    # Guruhni bazaga qo'shish
    await db.add_group(group_id, group_name)
    
    # Guruh tilini olish
    language = await get_group_language(db, group_id)
    lang_data = get_language_module(language)
    
    # Agar o'yin allaqachon boshlanган bo'lsa
    if group_id in active_games:
        await message.answer(lang_data.GAME_ALREADY_RUNNING)
        return
    
    # Yangi o'yin yaratish
    active_games[group_id] = {
        "players": [],
        "status": "waiting",
        "mode": "classic",
        "creator": message.from_user.id
    }
    
    game_text = f"""
🎮 **MAFIYA X - Yangi O'yin / New Game**

O'yinga qo'shilish uchun "✅ Qo'shilish" tugmasini bosing!
Click "✅ Join" to join the game!

👥 O'yinchilar / Players: 0
📊 Minimum: 4 o'yinchi kerak
"""
    
    await message.answer(
        game_text,
        reply_markup=get_game_join_keyboard(lang_data),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "join_game")
async def callback_join_game(callback: CallbackQuery):
    """O'yinga qo'shilish"""
    group_id = callback.message.chat.id
    user_id = callback.from_user.id
    user_name = callback.from_user.first_name
    
    if group_id not in active_games:
        await callback.answer("❌ O'yin topilmadi!", show_alert=True)
        return
    
    game = active_games[group_id]
    
    # Agar o'yinchi allaqachon qo'shilган bo'lsa
    if user_id in [p["id"] for p in game["players"]]:
        await callback.answer("⚠️ Siz allaqachon qo'shilgansiz!", show_alert=True)
        return
    
    # O'yinchini qo'shish
    game["players"].append({
        "id": user_id,
        "name": user_name,
        "role": None,
        "alive": True
    })
    
    # Matnni yangilash
    players_count = len(game["players"])
    players_list = "\n".join([f"{i+1}. {p['name']}" for i, p in enumerate(game["players"])])
    
    game_text = f"""
🎮 **MAFIYA X - Yangi O'yin / New Game**

O'yinga qo'shilish uchun "✅ Qo'shilish" tugmasini bosing!

👥 O'yinchilar / Players: {players_count}
📊 Minimum: 4 o'yinchi kerak

**Ro'yxat / List:**
{players_list}
"""
    
    language = await get_group_language(db, group_id)
    lang_data = get_language_module(language)
    
    await callback.message.edit_text(
        game_text,
        reply_markup=get_game_join_keyboard(lang_data),
        parse_mode="Markdown"
    )
    
    await callback.answer(f"✅ {user_name} qo'shildi!")

@router.callback_query(F.data == "leave_game")
async def callback_leave_game(callback: CallbackQuery):
    """O'yindan chiqish"""
    group_id = callback.message.chat.id
    user_id = callback.from_user.id
    
    if group_id not in active_games:
        await callback.answer("❌ O'yin topilmadi!", show_alert=True)
        return
    
    game = active_games[group_id]
    
    # O'yinchini o'chirish
    game["players"] = [p for p in game["players"] if p["id"] != user_id]
    
    # Matnni yangilash
    players_count = len(game["players"])
    players_list = "\n".join([f"{i+1}. {p['name']}" for i, p in enumerate(game["players"])]) if players_count > 0 else "Yo'q / None"
    
    game_text = f"""
🎮 **MAFIYA X - Yangi O'yin / New Game**

O'yinga qo'shilish uchun "✅ Qo'shilish" tugmasini bosing!

👥 O'yinchilar / Players: {players_count}
📊 Minimum: 4 o'yinchi kerak

**Ro'yxat / List:**
{players_list}
"""
    
    language = await get_group_language(db, group_id)
    lang_data = get_language_module(language)
    
    await callback.message.edit_text(
        game_text,
        reply_markup=get_game_join_keyboard(lang_data),
        parse_mode="Markdown"
    )
    
    await callback.answer("❌ O'yindan chiqdingiz!")

@router.callback_query(F.data == "start_game_now")
async def callback_start_game(callback: CallbackQuery):
    """O'yinni boshlash"""
    group_id = callback.message.chat.id
    user_id = callback.from_user.id
    
    if group_id not in active_games:
        await callback.answer("❌ O'yin topilmadi!", show_alert=True)
        return
    
    game = active_games[group_id]
    
    # Faqat o'yin yaratuvchisi boshlashi mumkin
    if user_id != game["creator"]:
        await callback.answer("⚠️ Faqat o'yin yaratuvchisi boshlashi mumkin!", show_alert=True)
        return
    
    # Minimum o'yinchilar soni tekshiruvi
    if len(game["players"]) < 4:
        await callback.answer("❌ Kamida 4 ta o'yinchi kerak!", show_alert=True)
        return
    
    # O'yinni boshlash
    game["status"] = "starting"
    
    language = await get_group_language(db, group_id)
    lang_data = get_language_module(language)
    
    await callback.message.edit_text(
        lang_data.GAME_STARTING + "\n\n⏳ 5 soniyada boshlanadi...",
        parse_mode="Markdown"
    )
    
    await asyncio.sleep(5)
    
    # Rollarni tarqatish (oddiy versiya)
    await assign_roles(group_id)
    
    await callback.answer()

async def assign_roles(group_id: int):
    """Rollarni tarqatish"""
    game = active_games[group_id]
    players = game["players"]
    players_count = len(players)
    
    # Oddiy rol taqsimoti
    # 1 Don, 1 Komissar, 1 Mafiya (agar 5+ o'yinchi bo'lsa), qolganlari Tinch aholi
    
    import random
    random.shuffle(players)
    
    roles_assigned = []
    
    # Don
    players[0]["role"] = "don"
    players[0]["team"] = "mafia"
    roles_assigned.append(("don", players[0]["id"]))
    
    # Komissar
    players[1]["role"] = "komissar"
    players[1]["team"] = "citizen"
    roles_assigned.append(("komissar", players[1]["id"]))
    
    # Agar 5+ o'yinchi bo'lsa, yana 1 mafiya
    if players_count >= 5:
        players[2]["role"] = "mafia"
        players[2]["team"] = "mafia"
        roles_assigned.append(("mafia", players[2]["id"]))
        start_idx = 3
    else:
        start_idx = 2
    
    # Qolganlari tinch aholi
    for i in range(start_idx, players_count):
        players[i]["role"] = "citizen"
        players[i]["team"] = "citizen"
        roles_assigned.append(("citizen", players[i]["id"]))
    
    # Har bir o'yinchiga rolini yuborish
    language = await get_group_language(db, group_id)
    lang_data = get_language_module(language)
    
    from aiogram import Bot
    from config import BOT_TOKEN
    bot = Bot(token=BOT_TOKEN)
    
    for role, user_id in roles_assigned:
        role_name = getattr(lang_data, f"ROLE_{role.upper()}", role)
        try:
            await bot.send_message(
                user_id,
                lang_data.ROLE_ASSIGNED.format(role=role_name)
            )
        except:
            pass
    
    # O'yin boshlanganligini e'lon qilish
    await bot.send_message(
        group_id,
        f"✅ {lang_data.GAME_STARTED}\n\n🌙 Tun boshlanadi..."
    )
    
    # O'yin jarayonini boshlash (keyingi bosqichda)
    game["status"] = "night"
