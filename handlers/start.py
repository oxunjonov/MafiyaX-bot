from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.db import db
from utils.language import get_language_module, get_user_language
from keyboards.inline import get_main_menu, get_language_keyboard, get_back_button

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Start buyrug'i"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    # Foydalanuvchini bazaga qo'shish
    await db.add_user(user_id, username, first_name)
    
    # Tilni olish
    language = await get_user_language(db, user_id)
    lang_data = get_language_module(language)
    
    # Inline keyboard - Guruhga qo'shish tugmasi bilan
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Guruhga qo'shish / Add to Group",
                url=f"https://t.me/{(await message.bot.me()).username}?startgroup=true"
            )
        ],
        [
            InlineKeyboardButton(
                text=lang_data.BTN_HELP,
                callback_data="help"
            ),
            InlineKeyboardButton(
                text=lang_data.BTN_RULES,
                callback_data="rules"
            )
        ],
        [
            InlineKeyboardButton(
                text=lang_data.BTN_LANGUAGE,
                callback_data="change_language"
            ),
            InlineKeyboardButton(
                text=lang_data.BTN_PROFILE,
                callback_data="profile"
            )
        ]
    ])
    
    # Javob yuborish
    await message.answer(
        lang_data.START_MESSAGE,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Help buyrug'i"""
    user_id = message.from_user.id
    language = await get_user_language(db, user_id)
    lang_data = get_language_module(language)
    
    await message.answer(
        lang_data.HELP_MESSAGE,
        reply_markup=get_back_button(lang_data),
        parse_mode="Markdown"
    )

@router.message(Command("rules"))
async def cmd_rules(message: Message):
    """Rules buyrug'i"""
    user_id = message.from_user.id
    language = await get_user_language(db, user_id)
    lang_data = get_language_module(language)
    
    await message.answer(
        lang_data.RULES_MESSAGE,
        reply_markup=get_back_button(lang_data),
        parse_mode="Markdown"
    )

@router.message(Command("language"))
async def cmd_language(message: Message):
    """Til o'zgartirish buyrug'i"""
    user_id = message.from_user.id
    language = await get_user_language(db, user_id)
    lang_data = get_language_module(language)
    
    await message.answer(
        lang_data.SELECT_LANGUAGE,
        reply_markup=get_language_keyboard()
    )

@router.callback_query(F.data.startswith("lang_"))
async def process_language_change(callback: CallbackQuery):
    """Til o'zgartirish callback"""
    user_id = callback.from_user.id
    new_language = callback.data.split("_")[1]
    
    # Tilni yangilash
    await db.update_language(user_id, new_language)
    
    # Yangi til ma'lumotlarini olish
    lang_data = get_language_module(new_language)
    
    await callback.message.edit_text(
        lang_data.LANGUAGE_CHANGED + "\n\n" + lang_data.START_MESSAGE,
        reply_markup=get_main_menu(lang_data),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "change_language")
async def callback_change_language(callback: CallbackQuery):
    """Til o'zgartirish tugmasi callback"""
    user_id = callback.from_user.id
    language = await get_user_language(db, user_id)
    lang_data = get_language_module(language)
    
    await callback.message.edit_text(
        lang_data.SELECT_LANGUAGE,
        reply_markup=get_language_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "help")
async def callback_help(callback: CallbackQuery):
    """Help callback"""
    user_id = callback.from_user.id
    language = await get_user_language(db, user_id)
    lang_data = get_language_module(language)
    
    await callback.message.edit_text(
        lang_data.HELP_MESSAGE,
        reply_markup=get_back_button(lang_data),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "rules")
async def callback_rules(callback: CallbackQuery):
    """Rules callback"""
    user_id = callback.from_user.id
    language = await get_user_language(db, user_id)
    lang_data = get_language_module(language)
    
    await callback.message.edit_text(
        lang_data.RULES_MESSAGE,
        reply_markup=get_back_button(lang_data),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_menu")
async def callback_back_to_menu(callback: CallbackQuery):
    """Asosiy menyuga qaytish"""
    user_id = callback.from_user.id
    language = await get_user_language(db, user_id)
    lang_data = get_language_module(language)
    
    await callback.message.edit_text(
        lang_data.START_MESSAGE,
        reply_markup=get_main_menu(lang_data),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.message(Command("profile"))
async def cmd_profile(message: Message):
    """Profil ko'rish buyrug'i"""
    user_id = message.from_user.id
    language = await get_user_language(db, user_id)
    lang_data = get_language_module(language)
    
    user = await db.get_user(user_id)
    
    if user:
        profile_text = f"""
👤 **Profil / Profile**

🆔 ID: `{user['user_id']}`
👤 Ism / Name: {user['first_name']}
🌍 Til / Language: {user['language'].upper()}

💎 Olmoslar / Diamonds: {user['diamonds']}
💵 Dollar / Balance: {user['balance']}

🎮 O'yinlar / Games: {user['games_played']}
🏆 G'alabalar / Wins: {user['games_won']}
"""
        await message.answer(profile_text, parse_mode="Markdown")
    else:
        await message.answer(lang_data.ERROR_OCCURRED)

@router.message(Command("myrole"))
async def cmd_myrole(message: Message):
    """Rolni ko'rish - o'yin davomida"""
    from utils.game_manager import game_manager
    from config import ROLE_EMOJI
    
    user_id = message.from_user.id
    language = await get_user_language(db, user_id)
    lang_data = get_language_module(language)
    
    # Barcha guruhlardagi o'yinlarni tekshirish
    user_role_info = None
    user_game_group = None
    
    for group_id, game in game_manager.games.items():
        if game.status in ["registration", "starting", "night", "day", "voting"]:
            player = game.get_player(user_id)
            if player and player.role:
                user_role_info = player
                user_game_group = group_id
                break
    
    if not user_role_info:
        await message.answer(
            "❌ Siz hozir hech qanday o'yinda qatnashmayapsiz yoki rol hali tarqatilmagan!\n\n"
            "❌ You are not in any active game or roles haven't been assigned yet!"
        )
        return
    
    # Rol ma'lumotlari
    role_name = lang_data.__dict__.get(f"ROLE_{user_role_info.role.upper()}", user_role_info.role)
    role_icon = ROLE_EMOJI.get(user_role_info.role, "🎭")
    
    # Jamoa ma'lumoti
    if user_role_info.team == "mafia":
        team_info = lang_data.TEAM_MAFIA
    elif user_role_info.team == "citizen":
        team_info = lang_data.TEAM_CITIZEN
    else:
        team_info = lang_data.TEAM_INDEPENDENT
    
    # Rol vazifasi
    role_task = lang_data.__dict__.get(f"TASK_{user_role_info.role.upper()}", "O'yinda qatnashing")
    
    # Rol tavsifi
    role_description = f"Siz {role_name}siz!"
    
    role_text = lang_data.ROLE_NOTIFICATION.format(
        role_icon=role_icon,
        role_name=role_name,
        role_description=role_description,
        team_info=team_info,
        role_task=role_task
    )
    
    await message.answer(role_text, parse_mode="Markdown")

@router.callback_query(F.data == "profile")
async def callback_profile(callback: CallbackQuery):
    """Profil callback"""
    user_id = callback.from_user.id
    user = await db.get_user(user_id)
    
    if user:
        profile_text = f"""
👤 **Profil / Profile**

🆔 ID: `{user['user_id']}`
👤 Ism / Name: {user['first_name']}
🌍 Til / Language: {user['language'].upper()}

💎 Olmoslar / Diamonds: {user['diamonds']}
💵 Dollar / Balance: {user['balance']}

🎮 O'yinlar / Games: {user['games_played']}
🏆 G'alabalar / Wins: {user['games_won']}
"""
        await callback.message.edit_text(profile_text, parse_mode="Markdown")
    await callback.answer()
