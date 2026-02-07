# GAME HANDLER - PROFESSIONAL EDITION
# Barcha o'yin mexanikasi

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
from utils.night_engine import NightEngine
from utils.day_engine import DayEngine
from utils.voting_engine import VotingEngine
from config import REGISTRATION_TIME, MIN_PLAYERS, MAX_PLAYERS
import asyncio

router = Router()

# Global states
active_votings = {}  # {chat_id: VotingEngine}
active_night_actions = {}  # {chat_id: {player_id: action}}

def get_registration_keyboard(game_id: int):
    """Ro'yxatdan o'tish klaviaturasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Qo'shilish / Join",
                callback_data=f"join_{game_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Chiqish / Leave",
                callback_data=f"leave_{game_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🎮 Boshlash / Start",
                callback_data=f"start_{game_id}"
            ),
            InlineKeyboardButton(
                text="🛑 Bekor qilish / Cancel",
                callback_data=f"cancel_{game_id}"
            )
        ]
    ])

@router.message(Command("game"))
async def cmd_game(message: Message, bot: Bot):
    """O'yin yaratish - Professional"""
    # Guruh tekshiruvi
    if message.chat.type not in ["group", "supergroup"]:
        return
    
    group_id = message.chat.id
    group_name = message.chat.title
    user_id = message.from_user.id
    
    # Buyruqni o'chirish
    try:
        await bot.delete_message(group_id, message.message_id)
    except:
        pass
    
    # Guruhni bazaga qo'shish
    await db.add_group(group_id, group_name)
    
    # Til
    language = await get_group_language(db, group_id)
    lang_data = get_language_module(language)
    
    # O'yin mavjudligini tekshirish
    if game_manager.has_active_game(group_id):
        msg = await message.answer("⚠️ Bu guruhda allaqachon o'yin mavjud!")
        await asyncio.sleep(5)
        try:
            await bot.delete_message(group_id, msg.message_id)
        except:
            pass
        return
    
    # Yangi o'yin yaratish
    game = game_manager.create_game(
        group_id=group_id,
        group_name=group_name,
        creator_id=user_id,
        mode="classic"
    )
    
    # Progress bar
    progress_bar = "▱" * 10
    
    # Ro'yxatdan o'tish xabari
    reg_text = f"""
🎮 **MAFIYA X - O'yin ro'yxati**

👥 **O'yinchilar:** 0/{MAX_PLAYERS}
⏰ **Vaqt:** {REGISTRATION_TIME // 60}:00 qoldi
📊 **Minimum:** {MIN_PLAYERS} ta o'yinchi

{progress_bar}

**Ro'yxat:**
_Hozircha hech kim yo'q_
"""
    
    sent_msg = await bot.send_message(
        group_id,
        reg_text,
        reply_markup=get_registration_keyboard(group_id),
        parse_mode="Markdown"
    )
    
    # Xabarni track qilish
    message_cleaner.track(group_id, sent_msg.message_id)
    
    # Timer
    async def on_timer_end():
        await start_game_process(bot, group_id, lang_data)
    
    timer = timer_manager.create_timer(
        chat_id=group_id,
        bot=bot,
        duration=REGISTRATION_TIME,
        callback=on_timer_end
    )
    
    await timer.start()
    
    # Real-time updates
    asyncio.create_task(update_registration_message(bot, group_id, sent_msg.message_id, lang_data))

async def update_registration_message(bot: Bot, group_id: int, message_id: int, lang_data):
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
        total_time = REGISTRATION_TIME
        remaining = timer.get_remaining_time()
        progress = (total_time - remaining) / total_time
        filled = int(progress * 10)
        progress_bar = "▰" * filled + "▱" * (10 - filled)
        
        # O'yinchilar
        players_list = ""
        if game.players:
            for i, p in enumerate(game.players, 1):
                if p.username:
                    mention = f"[@{p.username}](tg://user?id={p.user_id})"
                else:
                    mention = f"[{p.first_name}](tg://user?id={p.user_id})"
                players_list += f"{i}. {mention}\n"
        else:
            players_list = "_Hozircha hech kim yo'q_"
        
        # Yangilangan matn
        reg_text = f"""
🎮 **MAFIYA X - O'yin ro'yxati**

👥 **O'yinchilar:** {len(game.players)}/{MAX_PLAYERS}
⏰ **Vaqt:** {timer.get_formatted_time()} qoldi

{progress_bar}

**Ro'yxat:**
{players_list}
"""
        
        try:
            await bot.edit_message_text(
                chat_id=group_id,
                message_id=message_id,
                text=reg_text,
                reply_markup=get_registration_keyboard(group_id),
                parse_mode="Markdown"
            )
        except:
            pass

@router.callback_query(F.data.startswith("join_"))
async def callback_join_game(callback: CallbackQuery, bot: Bot):
    """O'yinga qo'shilish"""
    group_id = callback.message.chat.id
    user_id = callback.from_user.id
    username = callback.from_user.username
    first_name = callback.from_user.first_name
    
    game = game_manager.get_game(group_id)
    if not game:
        await callback.answer("❌ O'yin topilmadi!", show_alert=True)
        return
    
    # Qo'shilish
    if game.add_player(user_id, username, first_name):
        await db.add_user(user_id, username, first_name)
        await callback.answer("✅ O'yinga qo'shildingiz!")
    else:
        if len(game.players) >= MAX_PLAYERS:
            await callback.answer(f"❌ O'yin to'lgan! Max {MAX_PLAYERS} ta.", show_alert=True)
        else:
            await callback.answer("⚠️ Siz allaqachon qo'shilgansiz!", show_alert=True)

@router.callback_query(F.data.startswith("leave_"))
async def callback_leave_game(callback: CallbackQuery):
    """O'yindan chiqish"""
    group_id = callback.message.chat.id
    user_id = callback.from_user.id
    
    game = game_manager.get_game(group_id)
    if not game:
        await callback.answer("❌ O'yin topilmadi!", show_alert=True)
        return
    
    if game.remove_player(user_id):
        await callback.answer("❌ O'yindan chiqdingiz!")
    else:
        await callback.answer("⚠️ Siz o'yinda emassiz!", show_alert=True)

@router.callback_query(F.data.startswith("start_"))
async def callback_start_game(callback: CallbackQuery, bot: Bot):
    """O'yinni boshlash"""
    group_id = callback.message.chat.id
    user_id = callback.from_user.id
    
    game = game_manager.get_game(group_id)
    if not game:
        await callback.answer("❌ O'yin topilmadi!", show_alert=True)
        return
    
    # Ruxsat
    is_creator = user_id == game.creator_id
    is_admin_user = await is_admin(bot, group_id, user_id)
    
    if not (is_creator or is_admin_user):
        await callback.answer("⚠️ Faqat yaratuvchi yoki admin boshlashi mumkin!", show_alert=True)
        return
    
    # Minimum tekshiruv
    if not game.can_start():
        await callback.answer(f"❌ Kamida {MIN_PLAYERS} ta o'yinchi kerak!", show_alert=True)
        return
    
    # Timer to'xtatish
    await timer_manager.stop_timer(group_id)
    
    # Boshlash
    language = await get_group_language(db, group_id)
    lang_data = get_language_module(language)
    await start_game_process(bot, group_id, lang_data)
    await callback.answer("🎮 O'yin boshlanmoqda!")

@router.callback_query(F.data.startswith("cancel_"))
async def callback_cancel_game(callback: CallbackQuery, bot: Bot):
    """O'yinni bekor qilish"""
    group_id = callback.message.chat.id
    user_id = callback.from_user.id
    
    game = game_manager.get_game(group_id)
    if not game:
        await callback.answer("❌ O'yin topilmadi!", show_alert=True)
        return
    
    # Ruxsat
    is_creator = user_id == game.creator_id
    is_admin_user = await is_admin(bot, group_id, user_id)
    
    if not (is_creator or is_admin_user):
        await callback.answer("⚠️ Faqat yaratuvchi yoki admin bekor qilishi mumkin!", show_alert=True)
        return
    
    # To'xtatish
    await timer_manager.stop_timer(group_id)
    game_manager.delete_game(group_id)
    await message_cleaner.delete_all(bot, group_id)
    
    await callback.answer("🛑 O'yin bekor qilindi!")
    await bot.send_message(group_id, "🛑 O'yin bekor qilindi.")

async def start_game_process(bot: Bot, group_id: int, lang_data):
    """O'yinni boshlash jarayoni - Professional"""
    game = game_manager.get_game(group_id)
    if not game or not game.can_start():
        return
    
    # Eski xabarlarni o'chirish (ro'yxat xabarlari)
    await message_cleaner.delete_all(bot, group_id)
    
    game.status = "starting"
    
    # Countdown - 5 soniya
    for i in range(5, 0, -1):
        progress = (5 - i) / 5
        filled = int(progress * 10)
        bar = "▰" * filled + "▱" * (10 - filled)
        
        text = f"""
🎮 **O'YIN BOSHLANMOQDA!**

⏰ **{i} soniyada** boshlanadi...

👥 Ishtirokchilar: **{len(game.players)} ta**
🎭 Rollar tarqatilmoqda...

{bar}
"""
        
        if i == 5:
            countdown_msg = await bot.send_message(group_id, text, parse_mode="Markdown")
        else:
            try:
                await countdown_msg.edit_text(text, parse_mode="Markdown")
            except:
                pass
        
        await asyncio.sleep(1)
    
    # Countdown xabarini o'chirish
    try:
        await bot.delete_message(group_id, countdown_msg.message_id)
    except:
        pass
    
    # Rollarni tarqatish
    player_count = len(game.players)
    optimal_roles = get_optimal_roles(player_count)
    
    import random
    random.shuffle(game.players)
    
    for i, player in enumerate(game.players):
        if i < len(optimal_roles):
            player.role = optimal_roles[i]
            role_config = ALL_ROLES.get(player.role)
            if role_config:
                player.team = role_config.team
    
    # Har bir o'yinchiga rolini yuborish
    await send_roles_to_players(bot, game, lang_data)
    
    # O'yin boshlandi - GIF va Rolni ko'rish tugmasi
    await announce_game_start(bot, group_id, game, lang_data)
    
    # O'yin statusini yangilash
    game.status = "night"
    game.day_number = 1
    
    # Birinchi tun
    await start_night_phase(bot, group_id, game, lang_data)

async def send_roles_to_players(bot: Bot, game, lang_data):
    """Rollarni yuborish"""
    for player in game.players:
        role_config = ALL_ROLES.get(player.role)
        if not role_config:
            continue
        
        role_emoji = role_config.emoji
        role_name = role_config.name_uz
        role_desc = role_config.description
        
        # Jamoa
        if player.team == "mafia":
            team_info = "🔴 **Jamoa:** Mafiya"
        elif player.team == "citizen":
            team_info = "🟢 **Jamoa:** Tinch aholi"
        else:
            team_info = "🟡 **Jamoa:** Mustaqil (Yakka)"
        
        role_text = f"""
🎭 **SIZNING ROLINGIZ**

{role_emoji} **{role_name}**

{team_info}

📝 **Tavsif:**
{role_desc}

Omad tilaymiz! 🍀
"""
        
        try:
            await bot.send_message(
                player.user_id,
                role_text,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Rol yuborishda xatolik {player.user_id}: {e}")

async def announce_game_start(bot: Bot, group_id: int, game, lang_data):
    """O'yin boshlanganini e'lon qilish"""
    # Rolni ko'rish tugmasi
    bot_me = await bot.me()
    role_button = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🎭 Rolni ko'rish / View Role",
                url=f"https://t.me/{bot_me.username}?start=myrole"
            )
        ]
    ])
    
    start_text = f"""
✅ **O'YIN BOSHLANDI!**

👥 **O'yinchilar:** {len(game.players)} ta

💡 **Rolni ko'rish uchun pastdagi tugmani bosing!**
"""
    
    await bot.send_message(
        group_id,
        start_text,
        parse_mode="Markdown",
        reply_markup=role_button
    )

async def start_night_phase(bot: Bot, group_id: int, game, lang_data):
    """Tun boshlash - Professional"""
    # GIF - Tun
    night_gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3BjZnVzOTF5YzJ6NGhxMmN3OWJ6czBraGN6YzN6NWF5Y3lvdGYxYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o6Zt6ML6BklcajjsA/giphy.gif"
    
    try:
        await bot.send_animation(
            group_id,
            animation=night_gif_url,
            caption=f"🌙 **TUN {game.day_number}**"
        )
    except:
        await bot.send_message(
            group_id,
            f"🌙 **TUN {game.day_number} BOSHLANDI**\n\nShahar uxlayapti...",
            parse_mode="Markdown"
        )
    
    # Night actions ni toplash
    active_night_actions[group_id] = {}
    
    # Har bir faol rolga tun harakati uchun xabar
    await send_night_action_prompts(bot, game)
    
    # 60 soniya kutish
    await asyncio.sleep(60)
    
    # Tun natijalarini qayta ishlash
    await process_night_results(bot, group_id, game, lang_data)

async def send_night_action_prompts(bot: Bot, game):
    """Tun harakatlari uchun xabarlar yuborish"""
    for player in game.get_alive_players():
        role_config = ALL_ROLES.get(player.role)
        if not role_config or not role_config.night_action:
            continue
        
        # Har bir rol uchun action prompt
        # (Keyingi versiyada to'liq implement)
        pass

async def process_night_results(bot: Bot, group_id: int, game, lang_data):
    """Tun natijalarini qayta ishlash"""
    night_engine = NightEngine(game)
    
    # Actions ni qo'shish (hozirda test uchun)
    # Real versiyada: active_night_actions dan olish
    
    # Natijalarni olish
    night_result = night_engine.process_night()
    night_engine.apply_results()
    
    # Kun boshlash
    day_engine = DayEngine(game, bot, group_id)
    winner = await day_engine.start_day(night_result, lang_data, game.day_number)
    
    if winner:
        await announce_winner(bot, group_id, winner, lang_data)
        game_manager.end_game(group_id, winner)
    else:
        # Keyingi tun
        game.day_number += 1
        game.status = "night"
        await start_night_phase(bot, group_id, game, lang_data)

async def announce_winner(bot: Bot, group_id: int, winner: str, lang_data):
    """G'olibni e'lon qilish"""
    if winner == "citizen":
        text = "🎉 **TINCH AHOLI G'ALABA QILDI!**\n\nBarcha mafiyalar yo'q qilindi!"
    elif winner == "mafia":
        text = "😈 **MAFIYA G'ALABA QILDI!**\n\nShahar mafiya qo'lida!"
    elif winner == "suitsid":
        text = "🤦 **SUITSID G'ALABA QILDI!**"
    else:
        text = f"🏆 **{winner.upper()} G'ALABA QILDI!**"
    
    await bot.send_message(group_id, text, parse_mode="Markdown")

@router.message(Command("stop"))
async def cmd_stop_game(message: Message, bot: Bot):
    """O'yinni to'xtatish"""
    if message.chat.type not in ["group", "supergroup"]:
        return
    
    # Buyruqni o'chirish
    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    
    game = game_manager.get_game(message.chat.id)
    if not game:
        return
    
    # Ruxsat
    is_creator = message.from_user.id == game.creator_id
    is_admin_user = await is_admin(bot, message.chat.id, message.from_user.id)
    
    if not (is_creator or is_admin_user):
        return
    
    # To'xtatish
    await timer_manager.stop_timer(message.chat.id)
    game_manager.end_game(message.chat.id)
    await message_cleaner.delete_all(bot, message.chat.id)
    
    await bot.send_message(message.chat.id, "🛑 O'yin to'xtatildi va tozalandi.")
