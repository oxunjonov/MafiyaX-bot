# NIGHT ACTION ENGINE
# Tun jarayonini boshqarish - Professional

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from utils.roles import ALL_ROLES

@dataclass
class NightAction:
    """Tunda bajarilgan harakat"""
    actor_id: int  # Kim bajaradi
    actor_role: str  # Qaysi rol
    target_id: Optional[int] = None  # Kimga (agar kerak bo'lsa)
    action_type: str = ""  # check, kill, heal, block, etc.
    success: bool = True
    result: Optional[str] = None
    
@dataclass
class NightResult:
    """Tun natijalari"""
    deaths: List[int] = field(default_factory=list)  # O'lganlar
    saved: List[int] = field(default_factory=list)  # Qutqarilganlar
    blocked: List[int] = field(default_factory=list)  # Bloklangan
    checked: Dict[int, str] = field(default_factory=dict)  # Tekshirilganlar {player_id: result}
    witnessed: Dict[int, List[int]] = field(default_factory=dict)  # Guvohlar {daydi_id: [visitors]}
    photos: Dict[int, List[int]] = field(default_factory=dict)  # Suratlar {photo_id: [visitors]}
    
    # Maxsus
    afsungar_kills: List[int] = field(default_factory=list)  # Afsungar o'lsa, o'ldirgan ham
    bori_transform: Dict[int, str] = field(default_factory=dict)  # Bo'ri transform {bori_id: new_role}
    ghazabkor_marked: Dict[int, List[int]] = field(default_factory=dict)  # {ghazabkor_id: [marked]}

class NightEngine:
    """
    Professional Night Action Processing Engine
    
    Priority order:
    0. Sehrgar (protection)
    1. Advokat (lawyer protection)
    2. Doktor (doctor heal)
    3. Don/Mafia (kill)
    4. Qotil, Yollanma Qotil, Robin Gud (kills)
    5. Komissar (check)
    6. Serjant (get info)
    7. Kezuvchi (block)
    8. Daydi (witness)
    9. Fotparatchi (photo)
    10. Ayg'oqchi (spy)
    11. Aferist (steal vote)
    12. G'azabkor (mark)
    """
    
    def __init__(self, game):
        self.game = game
        self.actions: List[NightAction] = []
        self.result = NightResult()
        
    def add_action(self, actor_id: int, actor_role: str, target_id: Optional[int] = None, action_type: str = ""):
        """Harakat qo'shish"""
        action = NightAction(
            actor_id=actor_id,
            actor_role=actor_role,
            target_id=target_id,
            action_type=action_type
        )
        self.actions.append(action)
    
    def process_night(self) -> NightResult:
        """
        Tunni qayta ishlash - ASOSIY FUNKSIYA
        
        Returns:
            NightResult: Tun natijalari
        """
        # Actions ni priority bo'yicha sort qilish
        self.actions.sort(key=lambda a: ALL_ROLES[a.actor_role].priority)
        
        # Har bir action ni qayta ishlash
        protected_by_sehrgar: Set[int] = set()
        protected_by_advokat: Set[int] = set()
        healed: Set[int] = set()
        blocked: Set[int] = set()
        kill_attempts: Dict[int, List[tuple]] = {}  # {target_id: [(killer_id, killer_role)]}
        
        for action in self.actions:
            actor = self.game.get_player(action.actor_id)
            if not actor or not actor.is_alive:
                continue
            
            # Bloklangan ekanligini tekshirish
            if actor.user_id in blocked:
                continue
            
            role = action.actor_role
            target_id = action.target_id
            
            # ==== PRIORITY 0: SEHRGAR ====
            if role == "sehrgar":
                # Sehrgar o'zini himoya qiladi (passive)
                protected_by_sehrgar.add(actor.user_id)
            
            # ==== PRIORITY 1: ADVOKAT ====
            elif role == "advokat" and target_id:
                protected_by_advokat.add(target_id)
            
            # ==== PRIORITY 2: DOKTOR ====
            elif role == "doctor" and target_id:
                target = self.game.get_player(target_id)
                if target and target.team == "citizen":
                    healed.add(target_id)
            
            # ==== PRIORITY 3-4: KILLS ====
            elif action.action_type == "kill" and target_id:
                if target_id not in kill_attempts:
                    kill_attempts[target_id] = []
                kill_attempts[target_id].append((actor.user_id, role))
            
            # ==== PRIORITY 5: KOMISSAR ====
            elif role == "komissar" and target_id:
                target = self.game.get_player(target_id)
                if target:
                    # Advokat himoyasi tekshiruvi
                    if target_id in protected_by_advokat and target.team == "mafia":
                        self.result.checked[target_id] = "citizen"
                    else:
                        self.result.checked[target_id] = target.team
            
            # ==== PRIORITY 7: KEZUVCHI ====
            elif role == "kezuvchi" and target_id:
                blocked.add(target_id)
                self.result.blocked.append(target_id)
            
            # ==== PRIORITY 8: DAYDI ====
            elif role == "daydi" and target_id:
                # Kimlar kelganini ko'rish
                visitors = []
                for other_action in self.actions:
                    if other_action.target_id == target_id and other_action.actor_id != actor.user_id:
                        visitors.append(other_action.actor_id)
                if visitors:
                    self.result.witnessed[actor.user_id] = visitors
            
            # ==== PRIORITY 9: FOTPARATCHI ====
            elif role == "fotparatchi" and target_id:
                # Target ning tungi harakatlarini suratga olish
                target_actions = [a for a in self.actions if a.actor_id == target_id]
                if target_actions:
                    photos = [a.target_id for a in target_actions if a.target_id]
                    if photos:
                        self.result.photos[actor.user_id] = photos
            
            # ==== PRIORITY 10: AYGOQCHI ====
            elif role == "aygoqchi" and target_id:
                # Target rolini bilish (mafiyaga oshkor)
                target = self.game.get_player(target_id)
                if target:
                    # Game state ga qo'shiladi (keyingi funksiya)
                    pass
            
            # ==== PRIORITY 12: G'AZABKOR ====
            elif role == "ghazabkor" and target_id:
                if actor.user_id not in self.result.ghazabkor_marked:
                    self.result.ghazabkor_marked[actor.user_id] = []
                self.result.ghazabkor_marked[actor.user_id].append(target_id)
        
        # O'lishlarni qayta ishlash
        for target_id, killers in kill_attempts.items():
            # Himoya tekshiruvi
            if target_id in healed:
                self.result.saved.append(target_id)
                continue
            
            if target_id in protected_by_sehrgar:
                # Sehrgar himoyasi - o'ldirgan o'ladi!
                for killer_id, killer_role in killers:
                    if killer_role in ["don", "mafia", "qotil"]:
                        self.result.deaths.append(killer_id)
                continue
            
            # Target o'ladi
            target = self.game.get_player(target_id)
            if target and target.is_alive:
                self.result.deaths.append(target_id)
                
                # Maxsus rol reaksiyalari
                # Afsungar - o'ldirgan ham o'ladi
                if target.role == "afsungar":
                    for killer_id, _ in killers:
                        if killer_id not in self.result.deaths:
                            self.result.deaths.append(killer_id)
                            self.result.afsungar_kills.append(killer_id)
                
                # Bo'ri - transform
                elif target.role == "bori":
                    if killers:
                        killer_id, killer_role = killers[0]
                        if killer_role in ["don", "mafia"]:
                            self.result.bori_transform[target_id] = "mafia"
                        elif killer_role == "komissar":
                            self.result.bori_transform[target_id] = "serjant"
                        # Qotil o'ldirsa, oddiy o'ladi
        
        return self.result
    
    def apply_results(self):
        """Natijalarni o'yinga qo'llash"""
        # O'lganlarni belgilash
        for player_id in self.result.deaths:
            player = self.game.get_player(player_id)
            if player:
                player.is_alive = False
        
        # Bo'ri transformatsiyasi
        for player_id, new_role in self.result.bori_transform.items():
            player = self.game.get_player(player_id)
            if player and player.is_alive:
                player.role = new_role
                if new_role == "mafia":
                    player.team = "mafia"
                elif new_role == "serjant":
                    player.team = "citizen"
    
    def get_night_summary(self, lang_data) -> str:
        """
        Tun xulosasi - kun boshlanganda ko'rsatish uchun
        """
        if not self.result.deaths and not self.result.saved:
            return "✨ **Bu tunda hech kim o'lmadi!**"
        
        lines = []
        
        # O'lganlar
        if self.result.deaths:
            lines.append("💀 **Bu tunda quyidagilar halok bo'ldi:**")
            for player_id in self.result.deaths:
                player = self.game.get_player(player_id)
                if player:
                    role_config = ALL_ROLES.get(player.role)
                    role_name = role_config.name_uz if role_config else player.role
                    role_emoji = role_config.emoji if role_config else "❓"
                    
                    # Mention qilish
                    mention = f"@{player.username}" if player.username else player.first_name
                    lines.append(f"{role_emoji} [{mention}](tg://user?id={player.user_id}) - {role_name}")
        
        # Qutqarilganlar (faqat statistika uchun, userga ko'rsatilmaydi)
        # if self.result.saved:
        #     lines.append("\n💚 Qutqarildi: ...")
        
        return "\n".join(lines)
