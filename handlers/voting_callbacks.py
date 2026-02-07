# VOTING CALLBACKS
# Ovoz berish - Professional

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from utils.game_manager import game_manager

router = Router()

# Global voting storage
voting_storage = {}  # {chat_id: {voter_id: candidate_id}}

def get_voting_keyboard_v2(game, voter_id=None):
    """
    Ovoz berish klaviaturasi - yangi versiya
    Har bir odam har kimga ovoz bera oladi
    """
    alive_players = game.get_alive_players()
    chat_id = game.group_id
    
    if chat_id not in voting_storage:
        voting_storage[chat_id] = {}
    
    votes = voting_storage[chat_id]
    
    buttons = []
    
    # Har bir o'yinchi uchun
    for player in alive_players:
        # Ism
        if player.username:
            name = f"@{player.username}"
        else:
            name = player.first_name
        
        # Ovozlar soni
        vote_count = sum(1 for v in votes.values() if v == player.user_id)
        
        # User ovozi
        user_voted = ""
        if voter_id and votes.get(voter_id) == player.user_id:
            user_voted = " ✅"
        
        button_text = f"{name} ({vote_count} ovoz){user_voted}"
        
        row = [
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"vote_{player.user_id}"
            )
        ]
        buttons.append(row)
    
    # Ovozni qaytarib olish
    if voter_id and voter_id in votes:
        buttons.append([
            InlineKeyboardButton(
                text="🔄 Ovozni qaytarib olish / Unvote",
                callback_data="vote_unvote"
            )
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_vote_summary(game):
    """
    Ovozlar xulosasi
    """
    alive_players = game.get_alive_players()
    chat_id = game.group_id
    
    if chat_id not in voting_storage:
        return "Hali hech kim ovoz bermagan."
    
    votes = voting_storage[chat_id]
    
    # Har bir nomzod uchun ovozlar
    vote_counts = {}
    for player in alive_players:
        vote_counts[player.user_id] = 0
    
    for candidate_id in votes.values():
        if candidate_id in vote_counts:
            vote_counts[candidate_id] += 1
    
    # Tartiblash
    sorted_candidates = sorted(vote_counts.items(), key=lambda x: x[1], reverse=True)
    
    lines = ["📊 **OVOZLAR:**\n"]
    
    for candidate_id, count in sorted_candidates:
        if count == 0:
            continue
        
        player = game.get_player(candidate_id)
        if not player:
            continue
        
        name = f"@{player.username}" if player.username else player.first_name
        lines.append(f"{name}: **{count} ovoz**")
    
    if len(lines) == 1:
        return "Hali hech kim ovoz bermagan."
    
    return "\n".join(lines)

def get_vote_details(game):
    """
    Kim kimga ovoz berdi - detallari
    """
    chat_id = game.group_id
    
    if chat_id not in voting_storage or not voting_storage[chat_id]:
        return "_Hali ovozlar yo'q_"
    
    votes = voting_storage[chat_id]
    lines = []
    
    for voter_id, candidate_id in votes.items():
        voter = game.get_player(voter_id)
        candidate = game.get_player(candidate_id)
        
        if not voter or not candidate:
            continue
        
        voter_name = f"@{voter.username}" if voter.username else voter.first_name
        candidate_name = f"@{candidate.username}" if candidate.username else candidate.first_name
        
        lines.append(f"• {voter_name} → {candidate_name}")
    
    return "\n".join(lines) if lines else "_Ovozlar yo'q_"

@router.callback_query(F.data.startswith("vote_"))
async def handle_vote(callback: CallbackQuery):
    """Ovoz berish callback"""
    user_id = callback.from_user.id
    
    # Bekor qilish
    if callback.data == "vote_unvote":
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
        
        if chat_id in voting_storage and user_id in voting_storage[chat_id]:
            del voting_storage[chat_id][user_id]
            await callback.answer("🔄 Ovoz qaytarildi!")
            
            # Keyboard yangilash
            try:
                keyboard = get_voting_keyboard_v2(game, user_id)
                await callback.message.edit_reply_markup(reply_markup=keyboard)
            except:
                pass
        else:
            await callback.answer("⚠️ Siz ovoz bermagansiz!", show_alert=True)
        
        return
    
    # Ovoz berish
    candidate_id = int(callback.data.split("_")[1])
    
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
    
    # O'ziga ovoz bera olmaslik
    if candidate_id == user_id:
        await callback.answer("❌ O'zingizga ovoz bera olmaysiz!", show_alert=True)
        return
    
    # Tirikligini tekshirish
    voter = game.get_player(user_id)
    candidate = game.get_player(candidate_id)
    
    if not voter or not voter.is_alive:
        await callback.answer("❌ Siz o'yin ichida emassiz!", show_alert=True)
        return
    
    if not candidate or not candidate.is_alive:
        await callback.answer("❌ Bu odam allaqachon o'lgan!", show_alert=True)
        return
    
    # Ovoz berish
    if chat_id not in voting_storage:
        voting_storage[chat_id] = {}
    
    voting_storage[chat_id][user_id] = candidate_id
    
    candidate_name = f"@{candidate.username}" if candidate.username else candidate.first_name
    await callback.answer(f"✅ Ovoz berildi: {candidate_name}")
    
    # Keyboard yangilash
    try:
        keyboard = get_voting_keyboard_v2(game, user_id)
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except:
        pass

def calculate_voting_result(game):
    """
    Ovoz berish natijasini hisoblash
    
    Returns:
        hanged_id: Osilgan odam ID (yoki None)
        was_draw: Durrang bo'ldimi
    """
    chat_id = game.group_id
    
    if chat_id not in voting_storage or not voting_storage[chat_id]:
        return None, False
    
    votes = voting_storage[chat_id]
    
    # Ovozlarni hisoblash
    vote_counts = {}
    for candidate_id in votes.values():
        vote_counts[candidate_id] = vote_counts.get(candidate_id, 0) + 1
    
    if not vote_counts:
        return None, False
    
    # Eng ko'p ovoz
    max_votes = max(vote_counts.values())
    
    # Eng ko'p ovoz olganlar
    candidates_with_max = [cid for cid, count in vote_counts.items() if count == max_votes]
    
    if len(candidates_with_max) > 1:
        # Durrang
        return None, True
    
    # Bitta g'olib
    return candidates_with_max[0], False

def clear_voting(chat_id):
    """Ovozlarni tozalash"""
    if chat_id in voting_storage:
        voting_storage[chat_id] = {}
