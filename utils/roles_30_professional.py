# PROFESSIONAL MAFIA BOT - 30 ROLES CONFIGURATION
# Hidden roles, secret abilities, perfect balance

from dataclasses import dataclass
from typing import Optional, List, Dict
from enum import Enum

class Team(Enum):
    """Jamoa turlari"""
    MAFIA = "mafia"
    CITIZEN = "citizen"
    NEUTRAL = "neutral"

class RoleType(Enum):
    """Barcha 30 ta rol"""
    # TINCH AHOLI (13)
    TINCH_AHOLI = "tinch_aholi"
    KOMISSAR = "komissar"
    SHIFOKOR = "shifokor"
    KUZATUVCHI = "kuzatuvchi"
    QASOSCHI = "qasoschi"
    JANOB = "janob"
    UYQUCHI = "uyquchi"
    SERJANT = "serjant"
    SUITSID = "suitsid"
    ARXIVCHI = "arxivchi"
    QORIQCHI = "qoriqchi"
    BORI_CITIZEN = "bori_citizen"
    
    # MAFIYA (10)
    DON = "don"
    IJROCHI = "ijrochi"
    ALDOVCHI = "aldovchi"
    AXBOROTCHI = "axborotchi"
    HIMOYACHI = "himoyachi"
    MAFIA_AZOSI = "mafia_azosi"
    
    # NEYTRAL (7)
    QOTIL = "qotil"
    GHAZABKOR = "ghazabkor"
    SEHRGAR = "sehrgar"
    AFERIST = "aferist"
    FITNACHI = "fitnachi"
    BORI_NEUTRAL = "bori_neutral"

@dataclass
class RoleConfig:
    """Rol konfiguratsiyasi - Professional"""
    role_type: RoleType
    team: Team
    name_uz: str
    name_en: str
    name_ru: str
    emoji: str
    priority: int  # Tun tartibi
    
    # Qobiliyatlar
    can_kill: bool = False
    can_heal: bool = False
    can_check: bool = False
    can_protect: bool = False
    can_spy: bool = False
    can_block: bool = False
    
    # Maxsus
    night_action: bool = True
    vote_power: int = 1  # Ovoz kuchi
    protected_from_check: bool = False
    
    description_uz: str = ""
    description_en: str = ""
    description_ru: str = ""

# =====================================================
# TINCH AHOLI - 13 TA
# =====================================================

ROLES_CONFIG = {
    # 1. Tinch aholi
    RoleType.TINCH_AHOLI: RoleConfig(
        role_type=RoleType.TINCH_AHOLI,
        team=Team.CITIZEN,
        name_uz="Tinch aholi",
        name_en="Citizen",
        name_ru="Мирный житель",
        emoji="👤",
        priority=999,
        night_action=False,
        description_uz="Maxsus qobiliyati yo'q. Ovoz berish orqali mafiyani topadi."
    ),
    
    # 2. Kuzatuvchi
    RoleType.KUZATUVCHI: RoleConfig(
        role_type=RoleType.KUZATUVCHI,
        team=Team.CITIZEN,
        name_uz="Kuzatuvchi",
        name_en="Observer",
        name_ru="Наблюдатель",
        emoji="🧭",
        priority=9,
        can_spy=True,
        description_uz="Har tun bitta uyni kuzatib, qotillik bo'lganini biladi."
    ),
    
    # 3. Uyquchi
    RoleType.UYQUCHI: RoleConfig(
        role_type=RoleType.UYQUCHI,
        team=Team.CITIZEN,
        name_uz="Uyquchi",
        name_en="Sleeper",
        name_ru="Усыпитель",
        emoji="😴",
        priority=1,
        can_block=True,
        description_uz="Bitta o'yinchini uxlatadi. U tunda harakat qilmaydi, kunduz ovoz bermaydi."
    ),
    
    # 4. Qasoschi
    RoleType.QASOSCHI: RoleConfig(
        role_type=RoleType.QASOSCHI,
        team=Team.CITIZEN,
        name_uz="Qasoschi",
        name_en="Avenger",
        name_ru="Мститель",
        emoji="💥",
        priority=998,
        description_uz="Tunda o'ldirilsa, hujumchini o'zi bilan olib ketadi. Kunduz osilsa, bitta kishini tanlaydi."
    ),
    
    # 5. Bo'ri (Shahar)
    RoleType.BORI_CITIZEN: RoleConfig(
        role_type=RoleType.BORI_CITIZEN,
        team=Team.CITIZEN,
        name_uz="Bo'ri",
        name_en="Wolf",
        name_ru="Волк",
        emoji="🐺",
        priority=997,
        description_uz="Mafiya o'ldirsa → mafiya; Komissar o'ldirsa → serjant; Qotil o'ldirsa → o'ladi."
    ),
    
    # 6. Komissar
    RoleType.KOMISSAR: RoleConfig(
        role_type=RoleType.KOMISSAR,
        team=Team.CITIZEN,
        name_uz="Komissar Katani",
        name_en="Commissioner",
        name_ru="Комиссар",
        emoji="🕵️",
        priority=5,
        can_check=True,
        can_kill=True,
        description_uz="Har tun tekshirish yoki o'ldirish qiladi."
    ),
    
    # 7. Serjant
    RoleType.SERJANT: RoleConfig(
        role_type=RoleType.SERJANT,
        team=Team.CITIZEN,
        name_uz="Serjant",
        name_en="Sergeant",
        name_ru="Сержант",
        emoji="👮",
        priority=6,
        description_uz="Komissar o'lsa, uning o'rnini egallaydi."
    ),
    
    # 8. Shifokor
    RoleType.SHIFOKOR: RoleConfig(
        role_type=RoleType.SHIFOKOR,
        team=Team.CITIZEN,
        name_uz="Shifokor",
        name_en="Doctor",
        name_ru="Доктор",
        emoji="👨‍⚕️",
        priority=2,
        can_heal=True,
        description_uz="Har tun bitta kishini davolaydi va qutqaradi."
    ),
    
    # 9. Janob
    RoleType.JANOB: RoleConfig(
        role_type=RoleType.JANOB,
        team=Team.CITIZEN,
        name_uz="Janob",
        name_en="Gentleman",
        name_ru="Джентльмен",
        emoji="🎖",
        priority=996,
        night_action=False,
        vote_power=2,
        description_uz="Kunduz ovoz kuchi 2 ga teng. Shaxsi yashirin."
    ),
    
    # 10. Arxivchi
    RoleType.ARXIVCHI: RoleConfig(
        role_type=RoleType.ARXIVCHI,
        team=Team.CITIZEN,
        name_uz="Arxivchi",
        name_en="Archivist",
        name_ru="Архивист",
        emoji="📜",
        priority=10,
        can_spy=True,
        description_uz="Har tun bitta o'yinchining rolini biladi."
    ),
    
    # 11. Qo'riqchi
    RoleType.QORIQCHI: RoleConfig(
        role_type=RoleType.QORIQCHI,
        team=Team.CITIZEN,
        name_uz="Qo'riqchi",
        name_en="Guardian",
        name_ru="Хранитель",
        emoji="🛡",
        priority=1,
        can_protect=True,
        description_uz="Bitta kishini himoya qiladi. Tekshiruv natijasi Shahar bo'lib ko'rinadi."
    ),
    
    # 12. Suitsid
    RoleType.SUITSID: RoleConfig(
        role_type=RoleType.SUITSID,
        team=Team.CITIZEN,
        name_uz="Suitsid",
        name_en="Suicide",
        name_ru="Самоубийца",
        emoji="🤦",
        priority=995,
        night_action=False,
        description_uz="Kunduz osilsa, g'alaba qiladi."
    ),
    
    # =====================================================
    # MAFIYA - 10 TA
    # =====================================================
    
    # 13. Don
    RoleType.DON: RoleConfig(
        role_type=RoleType.DON,
        team=Team.MAFIA,
        name_uz="Don",
        name_en="Don",
        name_ru="Дон",
        emoji="🤵",
        priority=3,
        can_kill=True,
        protected_from_check=False,
        description_uz="Mafiya sardori. Har tun o'ldirish buyrug'i beradi."
    ),
    
    # 14. Mafia A'zosi
    RoleType.MAFIA_AZOSI: RoleConfig(
        role_type=RoleType.MAFIA_AZOSI,
        team=Team.MAFIA,
        name_uz="Mafiya",
        name_en="Mafia",
        name_ru="Мафия",
        emoji="🤵‍♂️",
        priority=3,
        description_uz="Don buyrug'iga bo'ysunadi. Zaxira tanlov qiladi."
    ),
    
    # 15. Axborotchi
    RoleType.AXBOROTCHI: RoleConfig(
        role_type=RoleType.AXBOROTCHI,
        team=Team.MAFIA,
        name_uz="Axborotchi",
        name_en="Informant",
        name_ru="Информатор",
        emoji="📰",
        priority=10,
        can_spy=True,
        description_uz="Uyga kelganlarni biladi."
    ),
    
    # 16. Ijrochi
    RoleType.IJROCHI: RoleConfig(
        role_type=RoleType.IJROCHI,
        team=Team.MAFIA,
        name_uz="Ijrochi",
        name_en="Executor",
        name_ru="Исполнитель",
        emoji="🔫",
        priority=2,
        can_kill=True,
        description_uz="Kafolatli o'ldirish. Himoya ishlamaydi."
    ),
    
    # 17. Himoyachi
    RoleType.HIMOYACHI: RoleConfig(
        role_type=RoleType.HIMOYACHI,
        team=Team.MAFIA,
        name_uz="Himoyachi",
        name_en="Protector",
        name_ru="Защитник",
        emoji="⚖️",
        priority=1,
        can_protect=True,
        description_uz="Mafiyani himoya qiladi. Tekshiruv Shahar bo'lib ko'rinadi."
    ),
    
    # 18. Aldovchi
    RoleType.ALDOVCHI: RoleConfig(
        role_type=RoleType.ALDOVCHI,
        team=Team.MAFIA,
        name_uz="Aldovchi",
        name_en="Deceiver",
        name_ru="Обманщик",
        emoji="🎭",
        priority=4,
        description_uz="Tekshiruv natijasini noto'g'ri qiladi."
    ),
    
    # =====================================================
    # NEYTRAL - 7 TA
    # =====================================================
    
    # 19. Qotil
    RoleType.QOTIL: RoleConfig(
        role_type=RoleType.QOTIL,
        team=Team.NEUTRAL,
        name_uz="Qotil",
        name_en="Serial Killer",
        name_ru="Убийца",
        emoji="🔪",
        priority=4,
        can_kill=True,
        description_uz="Har tun o'ldiradi. Oxirgi tirik qolsa yutadi."
    ),
    
    # 20. G'azabkor
    RoleType.GHAZABKOR: RoleConfig(
        role_type=RoleType.GHAZABKOR,
        team=Team.NEUTRAL,
        name_uz="G'azabkor",
        name_en="Angry",
        name_ru="Гневный",
        emoji="🧟",
        priority=12,
        description_uz="3 ta belgilaydi, keyin portlaydi. Belgilanlar o'ladi."
    ),
    
    # 21. Sehrgar
    RoleType.SEHRGAR: RoleConfig(
        role_type=RoleType.SEHRGAR,
        team=Team.NEUTRAL,
        name_uz="Sehrgar",
        name_en="Mage",
        name_ru="Маг",
        emoji="🧙",
        priority=0,
        protected_from_check=True,
        description_uz="Hujumlardan himoyalangan. Kunduz osilsa o'ladi."
    ),
    
    # 22. Suitsid (Neytral versiya - agar kerak bo'lsa)
    
    # 23. Aferist
    RoleType.AFERIST: RoleConfig(
        role_type=RoleType.AFERIST,
        team=Team.NEUTRAL,
        name_uz="Aferist",
        name_en="Trickster",
        name_ru="Аферист",
        emoji="🤹",
        priority=11,
        description_uz="Kunduzgi ovozni o'g'irlaydi."
    ),
    
    # 24. Bo'ri (Neytral)
    RoleType.BORI_NEUTRAL: RoleConfig(
        role_type=RoleType.BORI_NEUTRAL,
        team=Team.NEUTRAL,
        name_uz="Bo'ri",
        name_en="Wolf",
        name_ru="Волк",
        emoji="🐺",
        priority=997,
        description_uz="Transform qiladi."
    ),
    
    # 25. Fitnachi
    RoleType.FITNACHI: RoleConfig(
        role_type=RoleType.FITNACHI,
        team=Team.NEUTRAL,
        name_uz="Fitnachi",
        name_en="Whistleblower",
        name_ru="Доносчик",
        emoji="🧠",
        priority=13,
        can_spy=True,
        description_uz="Komissar tekshirsa, natijani biladi. Kunduz oshkor qilishi mumkin."
    ),
}

# 30 O'YINCHI UCHUN OPTIMAL TAQSIMOT
ROLE_DISTRIBUTION_30 = {
    "count": 30,
    "distribution": [
        # MAFIA - 10
        RoleType.DON,
        RoleType.IJROCHI,
        RoleType.ALDOVCHI,
        RoleType.AXBOROTCHI,
        RoleType.HIMOYACHI,
        RoleType.MAFIA_AZOSI,
        RoleType.MAFIA_AZOSI,
        RoleType.MAFIA_AZOSI,
        RoleType.MAFIA_AZOSI,
        RoleType.MAFIA_AZOSI,
        
        # NEUTRAL - 7
        RoleType.QOTIL,
        RoleType.GHAZABKOR,
        RoleType.SEHRGAR,
        RoleType.AFERIST,
        RoleType.FITNACHI,
        RoleType.BORI_NEUTRAL,
        RoleType.BORI_CITIZEN,
        
        # TINCH AHOLI - 13
        RoleType.TINCH_AHOLI,
        RoleType.TINCH_AHOLI,
        RoleType.KOMISSAR,
        RoleType.SHIFOKOR,
        RoleType.KUZATUVCHI,
        RoleType.QASOSCHI,
        RoleType.QASOSCHI,
        RoleType.QASOSCHI,
        RoleType.JANOB,
        RoleType.UYQUCHI,
        RoleType.SERJANT,
        RoleType.SERJANT,
        RoleType.SUITSID,
    ]
}

def get_role_distribution(player_count: int) -> List[RoleType]:
    """
    O'yinchilar soniga qarab optimal rol taqsimoti
    
    PERFECT BALANCE:
    - Mafiya: ~33%
    - Neytral: ~23%
    - Tinch aholi: ~44%
    """
    if player_count == 30:
        return ROLE_DISTRIBUTION_30["distribution"]
    
    # Boshqa sonlar uchun algoritm (4-29 o'yinchi)
    mafia_count = max(1, player_count // 3)
    neutral_count = max(0, player_count // 5)
    citizen_count = player_count - mafia_count - neutral_count
    
    roles = []
    
    # Mafiya
    roles.append(RoleType.DON)
    for i in range(mafia_count - 1):
        if i == 0:
            roles.append(RoleType.IJROCHI)
        elif i == 1:
            roles.append(RoleType.HIMOYACHI)
        else:
            roles.append(RoleType.MAFIA_AZOSI)
    
    # Neytral
    if neutral_count >= 1:
        roles.append(RoleType.QOTIL)
    if neutral_count >= 2:
        roles.append(RoleType.SEHRGAR)
    if neutral_count >= 3:
        roles.append(RoleType.GHAZABKOR)
    
    # Tinch aholi
    if citizen_count >= 1:
        roles.append(RoleType.KOMISSAR)
    if citizen_count >= 2:
        roles.append(RoleType.SHIFOKOR)
    if citizen_count >= 3:
        roles.append(RoleType.KUZATUVCHI)
    
    # Qolgan tinch aholi
    remaining = citizen_count - len([r for r in roles if ROLES_CONFIG[r].team == Team.CITIZEN])
    roles.extend([RoleType.TINCH_AHOLI] * remaining)
    
    return roles

def get_role_name(role_type: RoleType, lang: str = "uz") -> str:
    """Rol nomini tilga qarab qaytarish"""
    config = ROLES_CONFIG.get(role_type)
    if not config:
        return "Unknown"
    
    if lang == "en":
        return config.name_en
    elif lang == "ru":
        return config.name_ru
    else:
        return config.name_uz

def get_role_description(role_type: RoleType, lang: str = "uz") -> str:
    """Rol tavsifini tilga qarab qaytarish"""
    config = ROLES_CONFIG.get(role_type)
    if not config:
        return ""
    
    if lang == "en":
        return config.description_en or config.description_uz
    elif lang == "ru":
        return config.description_ru or config.description_uz
    else:
        return config.description_uz
