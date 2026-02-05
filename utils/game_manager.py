from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import random

@dataclass
class Player:
    """O'yinchi ma'lumotlari"""
    user_id: int
    username: Optional[str]
    first_name: str
    role: Optional[str] = None
    team: Optional[str] = None
    is_alive: bool = True
    protected: bool = False  # Doktor himoyasi
    kills: int = 0
    votes_received: int = 0
    last_action: Optional[str] = None

@dataclass
class Game:
    """O'yin ma'lumotlari"""
    group_id: int
    group_name: str
    creator_id: int
    mode: str = "classic"
    status: str = "registration"  # registration, starting, night, day, voting, finished
    players: List[Player] = field(default_factory=list)
    min_players: int = 4
    max_players: int = 50
    registration_time: int = 300  # 5 daqiqa
    night_time: int = 60
    day_time: int = 120
    vote_time: int = 90
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    winner: Optional[str] = None
    day_number: int = 0
    mafia_target: Optional[int] = None
    komissar_check: Optional[int] = None
    doctor_save: Optional[int] = None
    
    def add_player(self, user_id: int, username: Optional[str], first_name: str) -> bool:
        """O'yinchini qo'shish"""
        # Allaqachon bor ekanligini tekshirish
        if any(p.user_id == user_id for p in self.players):
            return False
        
        # Maksimum chegara
        if len(self.players) >= self.max_players:
            return False
        
        player = Player(
            user_id=user_id,
            username=username,
            first_name=first_name
        )
        self.players.append(player)
        return True
    
    def remove_player(self, user_id: int) -> bool:
        """O'yinchini o'chirish"""
        initial_count = len(self.players)
        self.players = [p for p in self.players if p.user_id != user_id]
        return len(self.players) < initial_count
    
    def get_player(self, user_id: int) -> Optional[Player]:
        """O'yinchini topish"""
        for player in self.players:
            if player.user_id == user_id:
                return player
        return None
    
    def get_alive_players(self) -> List[Player]:
        """Tirik o'yinchilar"""
        return [p for p in self.players if p.is_alive]
    
    def get_players_by_team(self, team: str) -> List[Player]:
        """Jamoa bo'yicha o'yinchilar"""
        return [p for p in self.players if p.team == team and p.is_alive]
    
    def get_players_by_role(self, role: str) -> List[Player]:
        """Rol bo'yicha o'yinchilar"""
        return [p for p in self.players if p.role == role and p.is_alive]
    
    def can_start(self) -> bool:
        """O'yin boshlanishi mumkinmi"""
        return len(self.players) >= self.min_players
    
    def assign_roles(self):
        """Rollarni tarqatish - Smart algorithm"""
        player_count = len(self.players)
        
        if player_count < self.min_players:
            return False
        
        # Shuffle players
        random.shuffle(self.players)
        
        # Rol taqsimoti (balanced)
        # 4 kishi: 1 Don, 1 Komissar, 2 Tinch
        # 5 kishi: 1 Don, 1 Mafiya, 1 Komissar, 2 Tinch
        # 6 kishi: 1 Don, 1 Mafiya, 1 Komissar, 1 Doktor, 2 Tinch
        # 7+ kishi: 1 Don, 2 Mafiya, 1 Komissar, 1 Doktor, qolganlari Tinch
        
        idx = 0
        
        # Don
        self.players[idx].role = "don"
        self.players[idx].team = "mafia"
        idx += 1
        
        # Komissar
        self.players[idx].role = "komissar"
        self.players[idx].team = "citizen"
        idx += 1
        
        # Mafiya (5+ o'yinchi bo'lsa)
        if player_count >= 5:
            self.players[idx].role = "mafia"
            self.players[idx].team = "mafia"
            idx += 1
        
        # Doktor (6+ o'yinchi bo'lsa)
        if player_count >= 6:
            self.players[idx].role = "doctor"
            self.players[idx].team = "citizen"
            idx += 1
        
        # Qo'shimcha mafiya (7+ o'yinchi bo'lsa)
        if player_count >= 7:
            self.players[idx].role = "mafia"
            self.players[idx].team = "mafia"
            idx += 1
        
        # Qolganlari Tinch aholi
        for i in range(idx, player_count):
            self.players[i].role = "citizen"
            self.players[i].team = "citizen"
        
        return True
    
    def check_win_condition(self) -> Optional[str]:
        """G'alaba shartini tekshirish"""
        alive_citizens = len(self.get_players_by_team("citizen"))
        alive_mafia = len(self.get_players_by_team("mafia"))
        
        # Mafiya g'alaba qildi
        if alive_mafia >= alive_citizens:
            return "mafia"
        
        # Tinch aholi g'alaba qildi
        if alive_mafia == 0:
            return "citizen"
        
        return None
    
    def get_stats(self) -> Dict:
        """O'yin statistikasi"""
        return {
            "total_players": len(self.players),
            "alive_players": len(self.get_alive_players()),
            "citizens": len(self.get_players_by_team("citizen")),
            "mafia": len(self.get_players_by_team("mafia")),
            "day_number": self.day_number,
            "duration": (datetime.now() - self.created_at).total_seconds() if self.created_at else 0
        }

class GameManager:
    """O'yinlarni boshqarish"""
    
    def __init__(self):
        self.games: Dict[int, Game] = {}
    
    def create_game(self, group_id: int, group_name: str, creator_id: int, mode: str = "classic") -> Game:
        """Yangi o'yin yaratish"""
        game = Game(
            group_id=group_id,
            group_name=group_name,
            creator_id=creator_id,
            mode=mode
        )
        self.games[group_id] = game
        return game
    
    def get_game(self, group_id: int) -> Optional[Game]:
        """O'yinni olish"""
        return self.games.get(group_id)
    
    def has_active_game(self, group_id: int) -> bool:
        """Aktiv o'yin bor ekanligini tekshirish"""
        game = self.games.get(group_id)
        return game is not None and game.status not in ["finished"]
    
    def end_game(self, group_id: int, winner: Optional[str] = None):
        """O'yinni tugatish"""
        if group_id in self.games:
            self.games[group_id].status = "finished"
            self.games[group_id].finished_at = datetime.now()
            self.games[group_id].winner = winner
    
    def delete_game(self, group_id: int):
        """O'yinni o'chirish"""
        if group_id in self.games:
            del self.games[group_id]
    
    def get_active_games_count(self) -> int:
        """Aktiv o'yinlar soni"""
        return len([g for g in self.games.values() if g.status != "finished"])

# Global instance
game_manager = GameManager()
