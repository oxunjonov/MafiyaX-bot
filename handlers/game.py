# GAME HANDLER - MUKAMMAL VERSIYA
# To'liq professional o'yin mexanikasi

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import db
from utils.language import get_language_module, get_group_language, get_user_language
from utils.permissions import is_admin
from utils.game_manager import game_manager
from utils.timer import timer_manager
from utils.cleaner import message_cleaner
from utils.roles import get_optimal_roles, ALL_ROLES
from config import REGISTRATION_TIME, MIN_PLAYERS, MAX_PLAYERS
import asyncio
import random

router = Router()

# Global states
night_actions_storage = {}  # {chat_id: {player_id: {"action": type, "target": id}}}
voting_storage = {}  # {chat_id: {voter_id: candidate_id}}
active_voting_messages = {}  # {chat_id: message_id}

def get_registration_keyboard(game_id: int):
    """Ro'yxatdan o'tish klaviaturasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Qo'shilish / Join", callback_data=f"join_{game_id}")],
        [InlineKeyboardButton(text="❌ Chiqish / Leave", callback_data=f"leave_{game_id}")],
        [
            InlineKeyboardButton(text="🎮 Boshlash / Start", callback_data=f"start_{game_id}"),
            InlineKeyboardButton(text="🛑 Bekor qilish / Cancel", callback_data=f"cancel_{game_id}")
        ]
    ])

@router.message(Command("game"))
async def cmd_game(message: Message, bot: Bot):
    """O'yin yaratish"""
    if message.chat.type not in ["group", "supergroup"]:
        return
    
    group_id = message.chat.id
    
    # Buyruqni o'chirish
    try:
        await bot.delete_message(group_id, message.message_id)
    except:
        pass
    
    # O'yin mavjudligini tekshirish
    if game_manager.has_active_game(group_id):
        msg = await bot.send_message(group_id, "⚠️ Bu guruhda allaqachon o'yin mavjud!")
        await asyncio.sleep(5)
        try:
            await bot.delete_message(group_id, msg.message_id)
        except:
            pass
        return
    
    # Guruhni bazaga qo'shish
    await db.add_group(group_id, message.chat.title)
    
    # Yangi o'yin yaratish
    game = game_manager.create_game(
        group_id=group_id,
        group_name=message.chat.title,
        creator_id=message.from_user.id,
        mode="classic"
    )
    
    # Ro'yxatdan o'tish xabari
    reg_text = f"""
🎮 **MAFIYA X - O'yin ro'yxati**

👥 **O'yinchilar:** 0/{MAX_PLAYERS}
⏰ **Vaqt:** {REGISTRATION_TIME // 60}:00 qoldi
📊 **Minimum:** {MIN_PLAYERS} ta o'yinchi

{'▱' * 10}

**Ro'yxat:**
_Hozircha hech kim yo'q_
"""
    
    sent_msg = await bot.send_message(group_id, reg_text, reply_markup=get_registration_keyboard(group_id), parse_mode="Markdown")
    message_cleaner.track(group_id, sent_msg.message_id)
    
    # Timer
    async def on_timer_end():
        await start_game_process(bot, group_id)
    
    timer = timer_manager.create_timer(chat_id=group_id, bot=bot, duration=REGISTRATION_TIME, callback=on_timer_end)
    await timer.start()
    
    # Real-time updates
    asyncio.create_task(update_registration_message(bot, group_id, sent_msg.message_id))

async def update_registration_message(bot: Bot, group_id: int, message_id: int):
    """Ro'yxat xabarini yangilash"""
    while timer_manager.has_timer(group_id):
        await asyncio.sleep(10)
        
        game = game_manager.get_game(group_id)
        if not game or game.status != "registration":
            break
        
        timer = timer_manager.get_timer(group_id)
        if not timer:
            break
        
        # Progress bar
        remaining = timer.get_remaining_time()
        progress = (REGISTRATION_TIME - remaining) / REGISTRATION_TIME
        filled = int(progress * 10)
        progress_bar = "▰" * filled + "▱" * (10 - filled)
        
        # O'yinchilar
        players_list = ""
        if game.players:
            for i, p in enumerate(game.players, 1):
                mention = f"[@{p.username}](tg://user?id={p.user_id})" if p.username else f"[{p.first_name}](tg://user?id={p.user_id})"
                players_list += f"{i}. {mention}\n"
        else:
            players_list = "_Hozircha hech kim yo'q_"
        
        reg_text = f"""
🎮 **MAFIYA X - O'yin ro'yxati**

👥 **O'yinchilar:** {len(game.players)}/{MAX_PLAYERS}
⏰ **Vaqt:** {timer.get_formatted_time()} qoldi

{progress_bar}

**Ro'yxat:**
{players_list}
"""
        
        try:
            await bot.edit_message_text(chat_id=group_id, message_id=message_id, text=reg_text, reply_markup=get_registration_keyboard(group_id), parse_mode="Markdown")
        except:
            pass

@router.callback_query(F.data.startswith("join_"))
async def callback_join_game(callback: CallbackQuery):
    """O'yinga qo'shilish"""
    game = game_manager.get_game(callback.message.chat.id)
    if not game:
        await callback.answer("❌ O'yin topilmadi!", show_alert=True)
        return
    
    if game.add_player(callback.from_user.id, callback.from_user.username, callback.from_user.first_name):
        await db.add_user(callback.from_user.id, callback.from_user.username, callback.from_user.first_name)
        await callback.answer("✅ O'yinga qo'shildingiz!")
    else:
        await callback.answer("⚠️ Qo'shilmadi! (To'lgan yoki allaqachon qo'shilgansiz)", show_alert=True)

@router.callback_query(F.data.startswith("leave_"))
async def callback_leave_game(callback: CallbackQuery):
    """O'yindan chiqish"""
    game = game_manager.get_game(callback.message.chat.id)
    if not game:
        await callback.answer("❌ O'yin topilmadi!", show_alert=True)
        return
    
    if game.remove_player(callback.from_user.id):
        await callback.answer("❌ O'yindan chiqdingiz!")
    else:
        await callback.answer("⚠️ Siz o'yinda emassiz!", show_alert=True)

@router.callback_query(F.data.startswith("start_"))
async def callback_start_game(callback: CallbackQuery, bot: Bot):
    """O'yinni boshlash"""
    group_id = callback.message.chat.id
    game = game_manager.get_game(group_id)
    
    if not game:
        await callback.answer("❌ O'yin topilmadi!", show_alert=True)
        return
    
    # Ruxsat tekshiruvi
    is_creator = callback.from_user.id == game.creator_id
    is_admin_user = await is_admin(bot, group_id, callback.from_user.id)
    
    if not (is_creator or is_admin_user):
        await callback.answer("⚠️ Faqat yaratuvchi yoki admin boshlashi mumkin!", show_alert=True)
        return
    
    if not game.can_start():
        await callback.answer(f"❌ Kamida {MIN_PLAYERS} ta o'yinchi kerak!", show_alert=True)
        return
    
    await timer_manager.stop_timer(group_id)
    await start_game_process(bot, group_id)
    await callback.answer("🎮 O'yin boshlanmoqda!")

@router.callback_query(F.data.startswith("cancel_"))
async def callback_cancel_game(callback: CallbackQuery, bot: Bot):
    """O'yinni bekor qilish"""
    group_id = callback.message.chat.id
    game = game_manager.get_game(group_id)
    
    if not game:
        await callback.answer("❌ O'yin topilmadi!", show_alert=True)
        return
    
    # Ruxsat
    is_creator = callback.from_user.id == game.creator_id
    is_admin_user = await is_admin(bot, group_id, callback.from_user.id)
    
    if not (is_creator or is_admin_user):
        await callback.answer("⚠️ Faqat yaratuvchi yoki admin bekor qilishi mumkin!", show_alert=True)
        return
    
    await timer_manager.stop_timer(group_id)
    game_manager.delete_game(group_id)
    await message_cleaner.delete_all(bot, group_id)
    
    await callback.answer("🛑 O'yin bekor qilindi!")
    await bot.send_message(group_id, "🛑 O'yin bekor qilindi.")

async def start_game_process(bot: Bot, group_id: int):
    """O'yinni boshlash - MUKAMMAL"""
    game = game_manager.get_game(group_id)
    if not game or not game.can_start():
        return
    
    # Eski xabarlarni o'chirish
    await message_cleaner.delete_all(bot, group_id)
    
    game.status = "starting"
    
    # Countdown
    for i in range(5, 0, -1):
        progress = (5 - i) / 5
        filled = int(progress * 10)
        bar = "▰" * filled + "▱" * (10 - filled)
        
        text = f"🎮 **O'YIN BOSHLANMOQDA!**\n\n⏰ **{i} soniyada** boshlanadi...\n\n{bar}"
        
        if i == 5:
            countdown_msg = await bot.send_message(group_id, text, parse_mode="Markdown")
        else:
            try:
                await countdown_msg.edit_text(text, parse_mode="Markdown")
            except:
                pass
        
        await asyncio.sleep(1)
    
    try:
        await bot.delete_message(group_id, countdown_msg.message_id)
    except:
        pass
    
    # Rollarni tarqatish
    optimal_roles = get_optimal_roles(len(game.players))
    random.shuffle(game.players)
    
    for i, player in enumerate(game.players):
        if i < len(optimal_roles):
            player.role = optimal_roles[i]
            role_config = ALL_ROLES.get(player.role)
            if role_config:
                player.team = role_config.team
    
    # Rollarniyuborish
    await send_roles_to_players(bot, game)
    
    # O'yin boshlandi
    bot_me = await bot.me()
    role_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎭 Rolni ko'rish / View Role", url=f"https://t.me/{bot_me.username}?start=myrole")]
    ])
    
    await bot.send_message(group_id, f"✅ **O'YIN BOSHLANDI!**\n\n👥 **O'yinchilar:** {len(game.players)} ta\n\n💡 **Rolni ko'rish uchun pastdagi tugmani bosing!**", parse_mode="Markdown", reply_markup=role_button)
    
    # O'yin boshlash
    game.status = "night"
    game.day_number = 1
    
    await start_night_phase(bot, group_id, game)

async def send_roles_to_players(bot: Bot, game):
    """Rollarni yuborish"""
    for player in game.players:
        role_config = ALL_ROLES.get(player.role)
        if not role_config:
            continue
        
        role_text = f"""
🎭 **SIZNING ROLINGIZ**

{role_config.emoji} **{role_config.name_uz}**

{'🔴 **Jamoa:** Mafiya' if player.team == 'mafia' else '🟢 **Jamoa:** Tinch aholi' if player.team == 'citizen' else '🟡 **Jamoa:** Mustaqil'}

📝 **Tavsif:**
{role_config.description}

Omad tilaymiz! 🍀
"""
        
        try:
            await bot.send_message(player.user_id, role_text, parse_mode="Markdown")
        except:
            pass

async def start_night_phase(bot: Bot, group_id: int, game):
    """Tun boshlash"""
    # GIF
    night_gif = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3BjZnVzOTF5YzJ6NGhxMmN3OWJ6czBraGN6YzN6NWF5Y3lvdGYxYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o6Zt6ML6BklcajjsA/giphy.gif"
    
    try:
        await bot.send_animation(group_id, animation=night_gif, caption=f"🌙 **TUN {game.day_number}**")
    except:
        await bot.send_message(group_id, f"🌙 **TUN {game.day_number} BOSHLANDI**\n\nShahar uxlayapti...", parse_mode="Markdown")
    
    # Night actions storage
    night_actions_storage[group_id] = {}
    
    # Har bir faol rolga xabar yuborish
    await send_night_action_requests(bot, game)
    
    # 60 soniya kutish
    await asyncio.sleep(60)
    
    # Tun natijalarini qayta ishlash
    await process_night_results(bot, group_id, game)

async def send_night_action_requests(bot: Bot, game):
    """Tun harakatlari uchun xabarlar"""
    alive = game.get_alive_players()
    
    for player in alive:
        role_config = ALL_ROLES.get(player.role)
        if not role_config or not role_config.night_action:
            continue
        
        # Target selection
        targets = [p for p in alive if p.user_id != player.user_id]
        buttons = []
        
        for target in targets:
            name = f"@{target.username}" if target.username else target.first_name
            buttons.append([InlineKeyboardButton(text=name, callback_data=f"night_{player.role}_{target.user_id}")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        # Rol bo'yicha xabar
        if player.role == "don":
            text = f"🤵 **DON**\n\n🌙 Tun boshlandi. Kimni o'ldirmoqchisiz?\n\nPastdagi ro'yxatdan tanlang:"
        elif player.role == "komissar":
            text = f"🕵️ **KOMISSAR**\n\n🌙 Kimni tekshirmoqchisiz?"
        elif player.role == "doctor":
            text = f"👨‍⚕️ **DOKTOR**\n\n🌙 Kimni davolashni xohlaysiz?"
        else:
            text = f"{role_config.emoji} **{role_config.name_uz.upper()}**\n\n🌙 Tun boshlandi. Harakatingizni tanlang:"
        
        try:
            await bot.send_message(player.user_id, text, reply_markup=keyboard, parse_mode="Markdown")
        except:
            pass

@router.callback_query(F.data.startswith("night_"))
async def handle_night_action(callback: CallbackQuery):
    """Tun harakati"""
    parts = callback.data.split("_")
    role = parts[1]
    target_id = int(parts[2])
    user_id = callback.from_user.id
    
    # O'yinni topish
    game = None
    for g in game_manager.games.values():
        if g.get_player(user_id):
            game = g
            break
    
    if not game:
        await callback.answer("❌ O'yin topilmadi!", show_alert=True)
        return
    
    # Saqlash
    night_actions_storage[game.group_id][user_id] = {"action": role, "target": target_id}
    
    target = game.get_player(target_id)
    target_name = f"@{target.username}" if target and target.username else (target.first_name if target else "?")
    
    await callback.message.edit_text(f"✅ Tanlandi: **{target_name}**\n\nTun tugashini kutib turing...", parse_mode="Markdown")
    await callback.answer("✅ Tanlandi!")

async def process_night_results(bot: Bot, group_id: int, game):
    """Tun natijalarini qayta ishlash"""
    actions = night_actions_storage.get(group_id, {})
    
    # O'lganlar
    deaths = []
    saved = []
    
    # Doktor davolagan
    for player_id, action in actions.items():
        if action["action"] == "doctor":
            saved.append(action["target"])
    
    # O'ldirishlar
    for player_id, action in actions.items():
        if action["action"] in ["don", "mafia", "qotil", "robin_gud", "yollanma_qotil"]:
            target_id = action["target"]
            if target_id not in saved and target_id not in deaths:
                deaths.append(target_id)
    
    # O'lganlarni belgilash
    for player_id in deaths:
        player = game.get_player(player_id)
        if player:
            player.is_alive = False
    
    # Kun boshlash
    await start_day_phase(bot, group_id, game, deaths)

async def start_day_phase(bot: Bot, group_id: int, game, deaths):
    """Kun boshlash"""
    # GIF
    day_gif = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDhsMnZiYzFyZGRxN2N4eXN5dGN4YnFyZjJvN2R3NWZqOGJ5cHprbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7btPCcdNniyf0ArS/giphy.gif"
    
    try:
        await bot.send_animation(group_id, animation=day_gif, caption=f"☀️ **KUN {game.day_number}**")
    except:
        await bot.send_message(group_id, f"☀️ **KUN {game.day_number} BOSHLANDI**", parse_mode="Markdown")
    
    await asyncio.sleep(2)
    
    # O'lganlar e'lon
    if deaths:
        lines = ["💀 **BU TUNDA QUYIDAGILAR HALOK BO'LDI:**\n"]
        for player_id in deaths:
            player = game.get_player(player_id)
            if player:
                role_config = ALL_ROLES.get(player.role)
                role_name = role_config.name_uz if role_config else player.role
                role_emoji = role_config.emoji if role_config else "❓"
                mention = f"[@{player.username}](tg://user?id={player.user_id})" if player.username else f"[{player.first_name}](tg://user?id={player.user_id})"
                lines.append(f"{role_emoji} {mention} - **{role_name}**")
        
        await bot.send_message(group_id, "\n".join(lines), parse_mode="Markdown")
    else:
        await bot.send_message(group_id, "✨ **Bu tunda hech kim o'lmadi!**", parse_mode="Markdown")
    
    await asyncio.sleep(2)
    
    # G'alaba tekshiruvi
    winner = game.check_win_condition()
    if winner:
        await announce_winner(bot, group_id, winner)
        game_manager.end_game(group_id, winner)
        return
    
    # Ovoz berish
    await start_voting_phase(bot, group_id, game)

async def start_voting_phase(bot: Bot, group_id: int, game):
    """Ovoz berish"""
    voting_storage[group_id] = {}
    alive = game.get_alive_players()
    
    # Klaviatura
    buttons = []
    for player in alive:
        name = f"@{player.username}" if player.username else player.first_name
        buttons.append([InlineKeyboardButton(text=f"{name} (0 ovoz)", callback_data=f"vote_{player.user_id}")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    vote_text = "🗳️ **OVOZ BERISH BOSHLANDI!**\n\n⏰ Vaqt: **40 soniya**\n\nKimni osmoqchisiz?"
    
    vote_msg = await bot.send_message(group_id, vote_text, reply_markup=keyboard, parse_mode="Markdown")
    active_voting_messages[group_id] = vote_msg.message_id
    
    # 40 soniya
    for i in range(8):
        await asyncio.sleep(5)
        
        # Update
        try:
            buttons = []
            votes_count = {}
            for voter_id, candidate_id in voting_storage.get(group_id, {}).items():
                votes_count[candidate_id] = votes_count.get(candidate_id, 0) + 1
            
            for player in alive:
                count = votes_count.get(player.user_id, 0)
                name = f"@{player.username}" if player.username else player.first_name
                buttons.append([InlineKeyboardButton(text=f"{name} ({count} ovoz)", callback_data=f"vote_{player.user_id}")])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            remaining = 40 - ((i + 1) * 5)
            
            await bot.edit_message_text(chat_id=group_id, message_id=vote_msg.message_id, text=f"🗳️ **OVOZ BERISH**\n\n⏰ Qoldi: **{remaining} soniya**", reply_markup=keyboard, parse_mode="Markdown")
        except:
            pass
    
    # Natija
    await announce_voting_result(bot, group_id, game)

@router.callback_query(F.data.startswith("vote_"))
async def handle_vote(callback: CallbackQuery):
    """Ovoz berish"""
    candidate_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    
    # O'yinni topish
    game = None
    for g in game_manager.games.values():
        if g.get_player(user_id):
            game = g
            break
    
    if not game:
        await callback.answer("❌ O'yin topilmadi!", show_alert=True)
        return
    
    if candidate_id == user_id:
        await callback.answer("❌ O'zingizga ovoz bera olmaysiz!", show_alert=True)
        return
    
    voting_storage[game.group_id][user_id] = candidate_id
    
    target = game.get_player(candidate_id)
    name = f"@{target.username}" if target and target.username else (target.first_name if target else "?")
    
    await callback.answer(f"✅ Ovoz: {name}")

async def announce_voting_result(bot: Bot, group_id: int, game):
    """Ovoz natijasi"""
    votes = voting_storage.get(group_id, {})
    
    if not votes:
        await bot.send_message(group_id, "❌ **HECH KIM OVOZ BERMADI!**", parse_mode="Markdown")
        game.day_number += 1
        game.status = "night"
        await start_night_phase(bot, group_id, game)
        return
    
    # Hisoblash
    vote_counts = {}
    for candidate_id in votes.values():
        vote_counts[candidate_id] = vote_counts.get(candidate_id, 0) + 1
    
    max_votes = max(vote_counts.values())
    winners = [cid for cid, count in vote_counts.items() if count == max_votes]
    
    if len(winners) > 1:
        await bot.send_message(group_id, "⚖️ **DURRANG!**\n\nHech kim osilmadi.", parse_mode="Markdown")
        game.day_number += 1
        game.status = "night"
        await start_night_phase(bot, group_id, game)
        return
    
    # Osilgan
    hanged_id = winners[0]
    hanged = game.get_player(hanged_id)
    
    if hanged:
        hanged.is_alive = False
        role_config = ALL_ROLES.get(hanged.role)
        role_name = role_config.name_uz if role_config else hanged.role
        role_emoji = role_config.emoji if role_config else "❓"
        mention = f"[@{hanged.username}](tg://user?id={hanged.user_id})" if hanged.username else f"[{hanged.first_name}](tg://user?id={hanged.user_id})"
        
        await bot.send_message(group_id, f"🪢 **OSILDI!**\n\n{role_emoji} {mention} - **{role_name}**", parse_mode="Markdown")
    
    # G'alaba
    winner = game.check_win_condition()
    if winner:
        await announce_winner(bot, group_id, winner)
        game_manager.end_game(group_id, winner)
    else:
        game.day_number += 1
        game.status = "night"
        await start_night_phase(bot, group_id, game)

async def announce_winner(bot: Bot, group_id: int, winner: str):
    """G'olib e'lon qilish"""
    if winner == "citizen":
        text = "🎉 **TINCH AHOLI G'ALABA QILDI!**\n\nBarcha mafiyalar yo'q qilindi!"
    elif winner == "mafia":
        text = "😈 **MAFIYA G'ALABA QILDI!**\n\nShahar mafiya qo'lida!"
    else:
        text = f"🏆 **{winner.upper()} G'ALABA QILDI!**"
    
    await bot.send_message(group_id, text, parse_mode="Markdown")

@router.message(Command("stop"))
async def cmd_stop_game(message: Message, bot: Bot):
    """O'yinni to'xtatish - MUKAMMAL TUZATILGAN"""
    if message.chat.type not in ["group", "supergroup"]:
        return
    
    group_id = message.chat.id
    user_id = message.from_user.id
    
    # Buyruqni o'chirish
    try:
        await bot.delete_message(group_id, message.message_id)
    except:
        pass
    
    # O'yin mavjudligini tekshirish
    game = game_manager.get_game(group_id)
    
    if not game:
        msg = await bot.send_message(group_id, "❌ Hozir o'yin yo'q!")
        await asyncio.sleep(3)
        try:
            await bot.delete_message(group_id, msg.message_id)
        except:
            pass
        return
    
    # Ruxsat tekshiruvi
    is_creator = user_id == game.creator_id
    is_admin_user = await is_admin(bot, group_id, user_id)
    
    if not (is_creator or is_admin_user):
        msg = await bot.send_message(group_id, "⚠️ Faqat yaratuvchi yoki admin to'xtatishi mumkin!")
        await asyncio.sleep(3)
        try:
            await bot.delete_message(group_id, msg.message_id)
        except:
            pass
        return
    
    # MUHIM: Timer ni to'xtatish
    if timer_manager.has_timer(group_id):
        await timer_manager.stop_timer(group_id)
    
    # MUHIM: O'yinni tugatish va o'chirish
    game.status = "finished"
    game_manager.end_game(group_id)
    
    # Storage larni tozalash
    if group_id in night_actions_storage:
        del night_actions_storage[group_id]
    if group_id in voting_storage:
        del voting_storage[group_id]
    if group_id in active_voting_messages:
        del active_voting_messages[group_id]
    
    # Xabarlarni tozalash
    await message_cleaner.delete_all(bot, group_id)
    
    # Tasdiqlash xabari
    confirm_msg = await bot.send_message(group_id, "🛑 **O'yin to'xtatildi va tozalandi.**", parse_mode="Markdown")
    
    # 5 soniyadan keyin tasdiqlash xabarini ham o'chirish
    await asyncio.sleep(5)
    try:
        await bot.delete_message(group_id, confirm_msg.message_id)
    except:
        pass
