# VOTING ENGINE
# Professional ovoz berish tizimi

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@dataclass
class Vote:
    """Bitta ovoz"""
    voter_id: int
    candidate_id: int
    vote_type: str  # "for" yoki "against"

@dataclass
class VotingResult:
    """Ovoz berish natijasi"""
    votes: Dict[int, Dict[str, int]] = field(default_factory=dict)  # {candidate_id: {"for": count, "against": count}}
    voters: Dict[int, int] = field(default_factory=dict)  # {voter_id: candidate_id} - kim kimga ovoz berdi
    hanged: Optional[int] = None
    was_draw: bool = False

class VotingEngine:
    """
    Professional Voting System
    - 40 soniya vaqt
    - Thumbs up/down
    - Real-time updates
    """
    
    def __init__(self, game, candidates: List[int]):
        self.game = game
        self.candidates = candidates  # Nomzodlar ro'yxati
        self.votes: Dict[int, Vote] = {}  # {voter_id: Vote}
        self.vote_counts: Dict[int, Dict[str, int]] = {}  # {candidate_id: {"for": 0, "against": 0}}
        
        # Initialize
        for candidate_id in candidates:
            self.vote_counts[candidate_id] = {"for": 0, "against": 0}
    
    def add_vote(self, voter_id: int, candidate_id: int, vote_type: str) -> bool:
        """
        Ovoz qo'shish
        
        Returns:
            bool: Muvaffaqiyatli qo'shildi yoki yo'q
        """
        # Avvalgi ovozni o'chirish
        if voter_id in self.votes:
            old_vote = self.votes[voter_id]
            self.vote_counts[old_vote.candidate_id][old_vote.vote_type] -= 1
        
        # Yangi ovoz
        vote = Vote(voter_id=voter_id, candidate_id=candidate_id, vote_type=vote_type)
        self.votes[voter_id] = vote
        self.vote_counts[candidate_id][vote_type] += 1
        
        return True
    
    def remove_vote(self, voter_id: int) -> bool:
        """Ovozni qaytarib olish"""
        if voter_id in self.votes:
            vote = self.votes[voter_id]
            self.vote_counts[vote.candidate_id][vote.vote_type] -= 1
            del self.votes[voter_id]
            return True
        return False
    
    def get_results(self) -> VotingResult:
        """
        Yakuniy natijalarni hisoblash
        """
        result = VotingResult()
        result.votes = self.vote_counts.copy()
        result.voters = {voter_id: vote.candidate_id for voter_id, vote in self.votes.items()}
        
        # Eng ko'p ovoz olgan nomzodni topish
        max_votes = -1
        max_candidate = None
        
        for candidate_id in self.candidates:
            net_votes = self.vote_counts[candidate_id]["for"] - self.vote_counts[candidate_id]["against"]
            
            if net_votes > max_votes:
                max_votes = net_votes
                max_candidate = candidate_id
            elif net_votes == max_votes and max_votes > 0:
                # Durrang!
                result.was_draw = True
        
        # Agar durrang bo'lmasa va ovozlar > 0
        if not result.was_draw and max_votes > 0:
            result.hanged = max_candidate
        
        return result
    
    def get_voting_keyboard(self, voter_id: int) -> InlineKeyboardMarkup:
        """
        Ovoz berish klaviaturasi
        """
        buttons = []
        
        # Har bir nomzod uchun 2 ta tugma (👍 va 👎)
        for candidate_id in self.candidates:
            candidate = self.game.get_player(candidate_id)
            if not candidate:
                continue
            
            # Mention
            name = f"@{candidate.username}" if candidate.username else candidate.first_name
            
            # Hozirgi ovozlar
            for_votes = self.vote_counts[candidate_id]["for"]
            against_votes = self.vote_counts[candidate_id]["against"]
            
            # User ovozi
            user_vote = None
            if voter_id in self.votes and self.votes[voter_id].candidate_id == candidate_id:
                user_vote = self.votes[voter_id].vote_type
            
            # Tugmalar
            for_text = f"👍 {for_votes}" + (" ✓" if user_vote == "for" else "")
            against_text = f"👎 {against_votes}" + (" ✓" if user_vote == "against" else "")
            
            row = [
                InlineKeyboardButton(
                    text=f"{name}",
                    callback_data=f"vote_info_{candidate_id}"
                ),
                InlineKeyboardButton(
                    text=for_text,
                    callback_data=f"vote_for_{candidate_id}"
                ),
                InlineKeyboardButton(
                    text=against_text,
                    callback_data=f"vote_against_{candidate_id}"
                )
            ]
            buttons.append(row)
        
        # Qaytarib olish tugmasi
        if voter_id in self.votes:
            buttons.append([
                InlineKeyboardButton(
                    text="🔄 Ovozni qaytarib olish / Unvote",
                    callback_data="vote_unvote"
                )
            ])
        
        return InlineKeyboardMarkup(inline_keyboard=buttons)
    
    def get_summary_text(self) -> str:
        """
        Ovoz berish xulosasi - real-time
        """
        lines = ["🗳️ **OVOZ BERISH**\n"]
        
        for candidate_id in self.candidates:
            candidate = self.game.get_player(candidate_id)
            if not candidate:
                continue
            
            name = f"@{candidate.username}" if candidate.username else candidate.first_name
            for_votes = self.vote_counts[candidate_id]["for"]
            against_votes = self.vote_counts[candidate_id]["against"]
            net = for_votes - against_votes
            
            # Progress bar
            total = for_votes + against_votes
            if total > 0:
                bar_length = 10
                for_bar = int((for_votes / total) * bar_length)
                against_bar = bar_length - for_bar
                bar = "🟩" * for_bar + "🟥" * against_bar
            else:
                bar = "⬜" * 10
            
            lines.append(f"{name}: {bar}")
            lines.append(f"   👍 {for_votes}  |  👎 {against_votes}  |  Net: {net:+d}\n")
        
        return "\n".join(lines)
