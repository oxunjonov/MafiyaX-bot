from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import db
from utils.language import get_language_module, get_group_language, get_user_language
from utils.permissions import is_admin, group_only
from utils.game_manager import game_manager, Player
from utils.timer import timer_manager
from utils.cleaner import message_cleaner
from config import REGISTRATION_TIME, MIN_PLAYERS, MAX_PLAYERS, ROLE_EMOJI
import asyncio

router = Router()

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
    """O'yin yaratish - faqat guruhlarda"""
    # Guruh tekshiruvi
    if message.chat.type not in ["group", "supergroup"]:
        user_id = message.from_user.id
        language = await get_user_language(db, user_id)
        lang_data = get_language_module(language)
        await message.answer(lang_data.ERROR_GROUP_ONLY)
        return
    
    group_id = message.chat.id
    group_name = message.chat.title
    user_id = message.from_user.id
    
    # Guruhni bazaga qo'shish
    await db.add_group(group_id, group_name)
    
    # Til
    language = await get_group_language(db, group_id)
    lang_data = get_language_module(language)
    
    # O'yin mavjudligini tekshirish
    if game_manager.has_active_game(group_id):
        await message.answer(lang_data.ERROR_GAME_EXISTS)
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
    reg_text = lang_data.REGISTRATION_STARTED.format(
        current=0,
        max=MAX_PLAYERS,
        min=MIN_PLAYERS,
        time=f"{REGISTRATION_TIME // 60}:00",
        progress_bar=progress_bar,
        players_list="_Hozircha hech kim yo'q_"
    )
    
    sent_msg = await message.answer(
        reg_text,
        reply_markup=get_registration_keyboard(group_id),
        parse_mode="Markdown"
    )
    
    # Xabarni track qilish
    message_cleaner.track(group_id, sent_msg.message_id)
    message_cleaner.track(group_id, message.message_id)
    
    # Timer yaratish va boshlash
    async def on_timer_end():
        """Timer tugaganda"""
        await start_game_process(bot, group_id, lang_data)
    
    timer = timer_manager.create_timer(
        chat_id=group_id,
        bot=bot,
        duration=REGISTRATION_TIME,
        callback=on_timer_end
    )
    
    await timer.start()
    
    # Timer updates (har 10 soniyada)
    asyncio.create_task(update_registration_message(bot, group_id, sent_msg.message_id, lang_data))

async def update_registration_message(bot: Bot, group_id: int, message_id: int, lang_data):
    """Ro'yxatdan o'tish xabarini yangilash"""
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
        
        # O'yinchilar ro'yxati
        if game.players:
            players_list = "\n".join([
                f"{i+1}. {p.first_name}" 
                for i, p in enumerate(game.players)
            ])
        else:
            players_list = "_Hozircha hech kim yo'q_"
        
        # Yangilangan matn
        reg_text = lang_data.REGISTRATION_UPDATE.format(
            current=len(game.players),
            max=MAX_PLAYERS,
            time=timer.get_formatted_time(),
            progress_bar=progress_bar,
            players_list=players_list
        )
        
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
    
    # Til
    language = await get_group_language(db, group_id)
    lang_data = get_language_module(language)
    
    # O'yinni olish
    game = game_manager.get_game(group_id)
    if not game:
        await callback.answer(lang_data.ERROR_NO_GAME, show_alert=True)
        return
    
    # Qo'shilish
    if game.add_player(user_id, username, first_name):
        # Foydalanuvchini bazaga qo'shish
        await db.add_user(user_id, username, first_name)
        await callback.answer(lang_data.SUCCESS_JOINED)
    else:
        if len(game.players) >= MAX_PLAYERS:
            await callback.answer(lang_data.ERROR_GAME_FULL.format(max=MAX_PLAYERS), show_alert=True)
        else:
            await callback.answer(lang_data.ERROR_ALREADY_JOINED, show_alert=True)

@router.callback_query(F.data.startswith("leave_"))
async def callback_leave_game(callback: CallbackQuery):
    """O'yindan chiqish"""
    group_id = callback.message.chat.id
    user_id = callback.from_user.id
    
    # Til
    language = await get_group_language(db, group_id)
    lang_data = get_language_module(language)
    
    # O'yinni olish
    game = game_manager.get_game(group_id)
    if not game:
        await callback.answer(lang_data.ERROR_NO_GAME, show_alert=True)
        return
    
    # Chiqish
    if game.remove_player(user_id):
        await callback.answer(lang_data.SUCCESS_LEFT)
    else:
        await callback.answer("❌ Siz o'yinda emassiz!", show_alert=True)

@router.callback_query(F.data.startswith("start_"))
async def callback_start_game(callback: CallbackQuery, bot: Bot):
    """O'yinni qo'lda boshlash"""
    group_id = callback.message.chat.id
    user_id = callback.from_user.id
    
    # Til
    language = await get_group_language(db, group_id)
    lang_data = get_language_module(language)
    
    # O'yinni olish
    game = game_manager.get_game(group_id)
    if not game:
        await callback.answer(lang_data.ERROR_NO_GAME, show_alert=True)
        return
    
    # Ruxsat tekshiruvi: creator yoki admin
    is_creator = user_id == game.creator_id
    is_admin_user = await is_admin(bot, group_id, user_id)
    
    if not (is_creator or is_admin_user):
        await callback.answer(lang_data.ERROR_GAME_CREATOR_ONLY, show_alert=True)
        return
    
    # Minimum o'yinchilar
    if not game.can_start():
        await callback.answer(
            lang_data.ERROR_NOT_ENOUGH_PLAYERS.format(min=MIN_PLAYERS),
            show_alert=True
        )
        return
    
    # Timer ni to'xtatish
    await timer_manager.stop_timer(group_id)
    
    # O'yinni boshlash
    await start_game_process(bot, group_id, lang_data)
    await callback.answer("🎮 O'yin boshlanmoqda!")

@router.callback_query(F.data.startswith("cancel_"))
async def callback_cancel_game(callback: CallbackQuery, bot: Bot):
    """O'yinni bekor qilish"""
    group_id = callback.message.chat.id
    user_id = callback.from_user.id
    
    # Til
    language = await get_group_language(db, group_id)
    lang_data = get_language_module(language)
    
    # O'yinni olish
    game = game_manager.get_game(group_id)
    if not game:
        await callback.answer(lang_data.ERROR_NO_GAME, show_alert=True)
        return
    
    # Ruxsat tekshiruvi
    is_creator = user_id == game.creator_id
    is_admin_user = await is_admin(bot, group_id, user_id)
    
    if not (is_creator or is_admin_user):
        await callback.answer(lang_data.ERROR_GAME_CREATOR_ONLY, show_alert=True)
        return
    
    # Timer to'xtatish
    await timer_manager.stop_timer(group_id)
    
    # O'yinni o'chirish
    game_manager.delete_game(group_id)
    
    # Xabarlarni tozalash
    await message_cleaner.delete_all(bot, group_id)
    
    await callback.answer("🛑 O'yin bekor qilindi!")
    await bot.send_message(group_id, "🛑 O'yin bekor qilindi.")

async def start_game_process(bot: Bot, group_id: int, lang_data):
    """O'yinni boshlash jarayoni"""
    game = game_manager.get_game(group_id)
    if not game:
        return
    
    # Minimum tekshiruv
    if not game.can_start():
        await bot.send_message(
            group_id,
            lang_data.ERROR_NOT_ENOUGH_PLAYERS.format(min=MIN_PLAYERS)
        )
        game_manager.delete_game(group_id)
        return
    
    # Status o'zgartirish
    game.status = "starting"
    
    # Countdown 5 soniya
    for i in range(5, 0, -1):
        progress = (5 - i) / 5
        filled = int(progress * 10)
        progress_bar = "▰" * filled + "▱" * (10 - filled)
        
        countdown_text = lang_data.GAME_STARTING_COUNTDOWN.format(
            seconds=i,
            count=len(game.players),
            progress_bar=progress_bar
        )
        
        if i == 5:
            msg = await bot.send_message(group_id, countdown_text, parse_mode="Markdown")
            countdown_msg_id = msg.message_id
        else:
            try:
                await bot.edit_message_text(
                    chat_id=group_id,
                    message_id=countdown_msg_id,
                    text=countdown_text,
                    parse_mode="Markdown"
                )
            except:
                pass
        
        await asyncio.sleep(1)
    
    # Rollarni tarqatish
    game.assign_roles()
    
    # Har bir o'yinchiga rolini yuborish (bot start bosmagan bo'lsa ham!)
    await send_roles_to_players(bot, game, lang_data)
    
    # O'yin boshlandi xabari
    await bot.send_message(
        group_id,
        f"✅ {lang_data.GAME_STARTED}\n\n🌙 **TUN 1** boshlandi...",
        parse_mode="Markdown"
    )
    
    # O'yin statusini yangilash
    game.status = "night"
    game.day_number = 1

async def send_roles_to_players(bot: Bot, game, lang_data):
    """Har bir o'yinchiga rolini yuborish"""
    for player in game.players:
        role_name = lang_data.__dict__.get(f"ROLE_{player.role.upper()}", player.role)
        role_icon = ROLE_EMOJI.get(player.role, "🎭")
        
        # Jamoa ma'lumoti
        if player.team == "mafia":
            team_info = lang_data.TEAM_MAFIA
        elif player.team == "citizen":
            team_info = lang_data.TEAM_CITIZEN
        else:
            team_info = lang_data.TEAM_INDEPENDENT
        
        # Rol vazifasi
        role_task = lang_data.__dict__.get(f"TASK_{player.role.upper()}", "O'yinda qatnashing")
        
        # Rol tavsifi (keyingi versiyada)
        role_description = f"Siz {role_name}siz!"
        
        role_text = lang_data.ROLE_NOTIFICATION.format(
            role_icon=role_icon,
            role_name=role_name,
            role_description=role_description,
            team_info=team_info,
            role_task=role_task
        )
        
        try:
            await bot.send_message(
                player.user_id,
                role_text,
                parse_mode="Markdown"
            )
        except Exception as e:
            # Agar bot bloklanган bo'lsa yoki boshqa xatolik
            print(f"Rol yuborishda xatolik {player.user_id}: {e}")

@router.message(Command("stop"))
async def cmd_stop_game(message: Message, bot: Bot):
    """O'yinni to'xtatish"""
    if message.chat.type not in ["group", "supergroup"]:
        return
    
    group_id = message.chat.id
    user_id = message.from_user.id
    
    # Til
    language = await get_group_language(db, group_id)
    lang_data = get_language_module(language)
    
    # O'yin mavjudligini tekshirish
    game = game_manager.get_game(group_id)
    if not game:
        await message.answer(lang_data.ERROR_NO_GAME)
        return
    
    # Ruxsat tekshiruvi
    is_creator = user_id == game.creator_id
    is_admin_user = await is_admin(bot, group_id, user_id)
    
    if not (is_creator or is_admin_user):
        await message.answer(lang_data.ERROR_GAME_CREATOR_ONLY)
        return
    
    # Timer to'xtatish
    await timer_manager.stop_timer(group_id)
    
    # O'yinni tugatish
    game_manager.end_game(group_id)
    
    # Xabarlarni tozalash
    await message_cleaner.delete_all(bot, group_id)
    
    await message.answer("🛑 O'yin to'xtatildi va tozalandi.")
