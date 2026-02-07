# NIGHT ACTION HANDLERS
# Har bir rol uchun tun harakatlari

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from utils.game_manager import game_manager
from utils.roles import ALL_ROLES

router = Router()

# Global storage for night actions
night_actions_storage = {}  # {chat_id: {player_id: {"action": "kill", "target": target_id}}}

def get_player_selection_keyboard(game, current_player_id, action_type: str):
    """
    O'yinchilarni tanlash klaviaturasi
    
    Args:
        game: O'yin obyekti
        current_player_id: Hozirgi o'yinchi (o'zi tanlanmasin)
        action_type: Harakat turi (kill, heal, check, etc.)
    """
    alive_players = game.get_alive_players()
    buttons = []
    
    for player in alive_players:
        if player.user_id == current_player_id:
            continue  # O'zini tanlay olmaydi
        
        # Ism
        if player.username:
            name = f"@{player.username}"
        else:
            name = player.first_name
        
        # Button
        button = InlineKeyboardButton(
            text=name,
            callback_data=f"night_action_{action_type}_{player.user_id}"
        )
        buttons.append([button])
    
    # Bekor qilish
    buttons.append([
        InlineKeyboardButton(
            text="❌ Bekor qilish / Cancel",
            callback_data=f"night_cancel_{action_type}"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def send_night_action_request(bot, player, game):
    """
    O'yinchiga tun harakati uchun so'rov yuborish
    """
    role_config = ALL_ROLES.get(player.role)
    if not role_config or not role_config.night_action:
        return
    
    chat_id = game.group_id
    
    # Initialize storage
    if chat_id not in night_actions_storage:
        night_actions_storage[chat_id] = {}
    
    # Har bir rol uchun alohida xabar
    if player.role == "don":
        text = f"""
🤵 **DON**

🌙 Tun boshlandi. Kimni o'ldirmoqchisiz?

Pastdagi ro'yxatdan tanlang:
"""
        keyboard = get_player_selection_keyboard(game, player.user_id, "don_kill")
        
        try:
            await bot.send_message(
                player.user_id,
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Don ga xabar yuborishda xatolik: {e}")
    
    elif player.role == "komissar":
        text = f"""
🕵️ **KOMISSAR KATANI**

🌙 Tun boshlandi. Kimni tekshirmoqchisiz?

Pastdagi ro'yxatdan tanlang:
"""
        keyboard = get_player_selection_keyboard(game, player.user_id, "komissar_check")
        
        try:
            await bot.send_message(
                player.user_id,
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Komissarga xabar yuborishda xatolik: {e}")
    
    elif player.role == "doctor":
        text = f"""
👨‍⚕️ **DOKTOR**

🌙 Tun boshlandi. Kimni davolashni xohlaysiz?

Pastdagi ro'yxatdan tanlang:
"""
        keyboard = get_player_selection_keyboard(game, player.user_id, "doctor_heal")
        
        try:
            await bot.send_message(
                player.user_id,
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Doktorga xabar yuborishda xatolik: {e}")
    
    elif player.role == "mafia":
        text = f"""
🤵‍♂️ **MAFIYA**

🌙 Tun boshlandi. Don buyrug'ini kutib turing.

Agar Don o'lgan bo'lsa, siz kimni o'ldirishni tanlaysiz:
"""
        # Agar Don tirik bo'lsa, mafiya kutadi
        don_alive = any(p.role == "don" and p.is_alive for p in game.players)
        
        if not don_alive:
            keyboard = get_player_selection_keyboard(game, player.user_id, "mafia_kill")
            try:
                await bot.send_message(
                    player.user_id,
                    text,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
            except:
                pass
        else:
            try:
                await bot.send_message(
                    player.user_id,
                    "🌙 Tun boshlandi. Don buyrug'ini kuting...",
                    parse_mode="Markdown"
                )
            except:
                pass
    
    elif player.role == "robin_gud":
        text = f"""
🏹 **ROBIN GUD**

🌙 Tun boshlandi. Kimni o'ldirmoqchisiz?

⚠️ Diqqat: Agar tinch bo'lmasa, xavfli!
"""
        keyboard = get_player_selection_keyboard(game, player.user_id, "robin_kill")
        
        try:
            await bot.send_message(
                player.user_id,
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except:
            pass
    
    elif player.role == "yollanma_qotil":
        text = f"""
🥷 **YOLLANMA QOTIL**

🌙 Tun boshlandi. Kimni o'ldirmoqchisiz?

⚠️ Komissar nishonga olsangiz, u sizni o'ldiradi!
"""
        keyboard = get_player_selection_keyboard(game, player.user_id, "hired_kill")
        
        try:
            await bot.send_message(
                player.user_id,
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except:
            pass
    
    elif player.role == "qotil":
        text = f"""
🔪 **QOTIL**

🌙 Tun boshlandi. Kimni o'ldirmoqchisiz?

Siz yakka o'ynaysiz!
"""
        keyboard = get_player_selection_keyboard(game, player.user_id, "serial_kill")
        
        try:
            await bot.send_message(
                player.user_id,
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except:
            pass
    
    elif player.role == "kezuvchi":
        text = f"""
💃 **KEZUVCHI**

🌙 Tun boshlandi. Kimga uyqu dorisi berasiz?

U kishi kunduz ovoz bera olmaydi.
"""
        keyboard = get_player_selection_keyboard(game, player.user_id, "kezuvchi_block")
        
        try:
            await bot.send_message(
                player.user_id,
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except:
            pass
    
    elif player.role == "daydi":
        text = f"""
🧙 **DAYDI**

🌙 Tun boshlandi. Qaysi uyga borasiz?

Kimlar kelganini ko'rasiz.
"""
        keyboard = get_player_selection_keyboard(game, player.user_id, "daydi_visit")
        
        try:
            await bot.send_message(
                player.user_id,
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except:
            pass
    
    elif player.role == "advokat":
        text = f"""
👨‍💼 **ADVOKAT**

🌙 Tun boshlandi. Kimni himoya qilasiz?

Agar mafiyani himoya qilsangiz, Komissar uni tinch deb ko'radi.
"""
        keyboard = get_player_selection_keyboard(game, player.user_id, "lawyer_protect")
        
        try:
            await bot.send_message(
                player.user_id,
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except:
            pass

# ===== CALLBACKS =====

@router.callback_query(F.data.startswith("night_action_"))
async def handle_night_action(callback: CallbackQuery):
    """Tun harakati callback"""
    data_parts = callback.data.split("_")
    # Format: night_action_{action_type}_{target_id}
    # Misol: night_action_don_kill_123456 → action=don_kill, target=vaqtinchalik
    
    # Hozircha simple version
    action_type = "_".join(data_parts[2:-1])  # don_kill, komissar_check, etc.
    target_id = int(data_parts[-1])
    
    user_id = callback.from_user.id
    
    # O'yinni topish
    game = None
    for g in game_manager.games.values():
        player = g.get_player(user_id)
        if player:
            game = g
            break
    
    if not game:
        await callback.answer("❌ O'yin topilmadi!", show_alert=True)
        return
    
    chat_id = game.group_id
    
    # Storage ga saqlash
    if chat_id not in night_actions_storage:
        night_actions_storage[chat_id] = {}
    
    night_actions_storage[chat_id][user_id] = {
        "action": action_type,
        "target": target_id
    }
    
    # Target nomi
    target = game.get_player(target_id)
    target_name = f"@{target.username}" if target and target.username else (target.first_name if target else "Unknown")
    
    # Tasdiqlash
    await callback.message.edit_text(
        f"✅ Tanlandi: **{target_name}**\n\nTun tugashini kutib turing...",
        parse_mode="Markdown"
    )
    await callback.answer("✅ Tanlandi!")

@router.callback_query(F.data.startswith("night_cancel_"))
async def handle_night_cancel(callback: CallbackQuery):
    """Tun harakatini bekor qilish"""
    await callback.message.edit_text(
        "❌ Bekor qilindi.\n\nBu tunda hech narsa qilmaysiz.",
        parse_mode="Markdown"
    )
    await callback.answer("❌ Bekor qilindi")
