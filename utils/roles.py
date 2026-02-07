# MAFIYA X - BARCHA ROLLAR
# Professional roles configuration

from dataclasses import dataclass
from typing import Optional, List

@dataclass
class RoleConfig:
    """Rol konfiguratsiyasi"""
    id: str
    name_uz: str
    name_ru: str
    emoji: str
    team: str  # citizen, mafia, singleton
    priority: int  # Tun tartib raqami (kim birinchi harakat qiladi)
    can_kill: bool = False
    can_heal: bool = False
    can_check: bool = False
    night_action: bool = True
    description: str = ""

# =====================================================
# TINCH AHOLI - 16 TA
# =====================================================

CITIZEN = RoleConfig(
    id="citizen",
    name_uz="Tinch aholi",
    name_ru="Мирный житель",
    emoji="👨",
    team="citizen",
    priority=999,
    night_action=False,
    description="Maxsus qobiliyati yo'q. Ovoz berish va mafiyani topishda ishtirok etadi."
)

KOMISSAR = RoleConfig(
    id="komissar",
    name_uz="Komissar Katani",
    name_ru="Комиссар Катани",
    emoji="🕵️",
    team="citizen",
    priority=5,
    can_check=True,
    description="Har tun 1 kishini tekshiradi, tinch yoki mafiya ekanligini biladi."
)

SERJANT = RoleConfig(
    id="serjant",
    name_uz="Serjant",
    name_ru="Сержант",
    emoji="👮",
    team="citizen",
    priority=6,
    description="Komissarning yordamchisi. Komissar o'lsa, uning o'rnini egallaydi."
)

DOCTOR = RoleConfig(
    id="doctor",
    name_uz="Doktor",
    name_ru="Доктор",
    emoji="👨‍⚕️",
    team="citizen",
    priority=2,
    can_heal=True,
    description="Har tun 1 kishini davolaydi. Agar tinch taraf bo'lsa, o'lmaydi."
)

DAYDI = RoleConfig(
    id="daydi",
    name_uz="Daydi",
    name_ru="Дядя",
    emoji="🧙",
    team="citizen",
    priority=8,
    description="Har tun xohlagan uyga boradi, qotillik guvohi bo'lishi mumkin."
)

KEZUVCHI = RoleConfig(
    id="kezuvchi",
    name_uz="Kezuvchi",
    name_ru="Странник",
    emoji="💃",
    team="citizen",
    priority=7,
    description="Har tun 1 kishiga uyqu dorisi beradi, kunduz ovoz bermaydi."
)

FOTPARATCHI = RoleConfig(
    id="fotparatchi",
    name_uz="Fotoparatchi",
    name_ru="Фотограф",
    emoji="📸",
    team="citizen",
    priority=9,
    description="Har tun 1 o'yinchining uyiga kim borganini rasmga oladi."
)

JANOB = RoleConfig(
    id="janob",
    name_uz="Janob",
    name_ru="Джентльмен",
    emoji="🎖",
    team="citizen",
    priority=999,
    night_action=False,
    description="Kunduzgi ovoz berishda ovozi 2 ga teng. Shaxsi oshkor bo'lmaydi."
)

ROBIN_GUD = RoleConfig(
    id="robin_gud",
    name_uz="Robin Gud",
    name_ru="Робин Гуд",
    emoji="🏹",
    team="citizen",
    priority=4,
    can_kill=True,
    description="Har tun 1 kishini o'ldiradi. Agar tinch bo'lmasa, xavfga duch keladi."
)

AFSUNGAR = RoleConfig(
    id="afsungar",
    name_uz="Afsungar",
    name_ru="Заклинатель",
    emoji="💣",
    team="citizen",
    priority=999,
    description="Tunda o'ldirilsa, o'ldirgan ham o'ladi. Kunduz osilsa, 1 kishini tanlaydi."
)

# =====================================================
# MAFIYA - 9 TA
# =====================================================

DON = RoleConfig(
    id="don",
    name_uz="Don",
    name_ru="Дон",
    emoji="🤵",
    team="mafia",
    priority=3,
    can_kill=True,
    description="Mafiya sardori. Har tun kim o'lishini hal qiladi."
)

MAFIA = RoleConfig(
    id="mafia",
    name_uz="Mafiya",
    name_ru="Мафия",
    emoji="🤵‍♂️",
    team="mafia",
    priority=3,
    description="Donga bo'ysunadi. Don o'lsa, ulardan biri Don bo'ladi."
)

ADVOKAT = RoleConfig(
    id="advokat",
    name_uz="Advokat",
    name_ru="Адвокат",
    emoji="👨‍💼",
    team="mafia",
    priority=1,
    description="Har tun 1 kishini himoya qiladi. Mafiyani himoya qilsa, Komissar uni tinch ko'radi."
)

YOLLANMA_QOTIL = RoleConfig(
    id="yollanma_qotil",
    name_uz="Yollanma Qotil",
    name_ru="Наемный убийца",
    emoji="🥷",
    team="mafia",
    priority=4,
    can_kill=True,
    description="Har tun 1 kishini yashirincha ovlaydi. Komissarni otsa, Komissar uni o'ldiradi."
)

AYGOQCHI = RoleConfig(
    id="aygoqchi",
    name_uz="Ayg'oqchi",
    name_ru="Шпион",
    emoji="🦇",
    team="mafia",
    priority=10,
    description="Har tun 1 o'yinchining rolini biladi va mafiyaga oshkor qiladi."
)

# =====================================================
# SINGLETON (YAKKA) - 7 TA
# =====================================================

QOTIL = RoleConfig(
    id="qotil",
    name_uz="Qotil",
    name_ru="Убийца",
    emoji="🔪",
    team="singleton",
    priority=4,
    can_kill=True,
    description="Faqat o'zi uchun o'ynaydi. Shaharni tozalash. Tirik qolsa yutadi."
)

SEHRGAR = RoleConfig(
    id="sehrgar",
    name_uz="Sehrgar",
    name_ru="Маг",
    emoji="🧙‍♂️",
    team="singleton",
    priority=0,
    description="O'z qonunlariga bo'ysunadi. Don/Qotil/Komissar o'ldira olmaydi."
)

SUITSID = RoleConfig(
    id="suitsid",
    name_uz="Suitsid",
    name_ru="Самоубийца",
    emoji="🤦",
    team="singleton",
    priority=999,
    night_action=False,
    description="Kunduz osib o'ldirilsa, darhol g'alaba qiladi."
)

AFERIST = RoleConfig(
    id="aferist",
    name_uz="Aferist",
    name_ru="Аферист",
    emoji="🤹",
    team="singleton",
    priority=11,
    description="Tunda 1 o'yinchining kunduzgi ovozini o'g'irlaydi."
)

BORI = RoleConfig(
    id="bori",
    name_uz="Bo'ri",
    name_ru="Волк",
    emoji="🐺",
    team="singleton",
    priority=999,
    description="Mafiya o'ldirsa→mafiya; Komissar o'ldirsa→serjant; Qotil o'ldirsa→o'ladi."
)

GHAZABKOR = RoleConfig(
    id="ghazabkor",
    name_uz="G'azabkor",
    name_ru="Гневный",
    emoji="🧟",
    team="singleton",
    priority=12,
    description="Har tun 1 kishini belgilaydi. 3 ta belgisa, portlaydi, belgilanlar o'ladi."
)

# =====================================================
# ROLLAR RO'YXATI
# =====================================================

ALL_ROLES = {
    # Tinch aholi
    "citizen": CITIZEN,
    "komissar": KOMISSAR,
    "serjant": SERJANT,
    "doctor": DOCTOR,
    "daydi": DAYDI,
    "kezuvchi": KEZUVCHI,
    "fotparatchi": FOTPARATCHI,
    "janob": JANOB,
    "robin_gud": ROBIN_GUD,
    "afsungar": AFSUNGAR,
    
    # Mafiya
    "don": DON,
    "mafia": MAFIA,
    "advokat": ADVOKAT,
    "yollanma_qotil": YOLLANMA_QOTIL,
    "aygoqchi": AYGOQCHI,
    
    # Singleton
    "qotil": QOTIL,
    "sehrgar": SEHRGAR,
    "suitsid": SUITSID,
    "aferist": AFERIST,
    "bori": BORI,
    "ghazabkor": GHAZABKOR,
}

# Rol taqsimoti - o'yinchilar soniga qarab
ROLE_DISTRIBUTION = {
    4: ["don", "komissar", "citizen", "citizen"],
    5: ["don", "mafia", "komissar", "citizen", "citizen"],
    6: ["don", "mafia", "komissar", "doctor", "citizen", "citizen"],
    7: ["don", "mafia", "mafia", "komissar", "doctor", "citizen", "citizen"],
    8: ["don", "mafia", "mafia", "komissar", "doctor", "daydi", "citizen", "citizen"],
    9: ["don", "mafia", "mafia", "komissar", "doctor", "daydi", "citizen", "citizen", "citizen"],
    10: ["don", "mafia", "mafia", "komissar", "serjant", "doctor", "daydi", "citizen", "citizen", "citizen"],
    # 11-30 uchun advanced algorithm
}

def get_optimal_roles(player_count: int) -> List[str]:
    """
    O'yinchilar soniga qarab optimal rollar ro'yxatini qaytaradi
    """
    if player_count <= 10:
        return ROLE_DISTRIBUTION.get(player_count, ROLE_DISTRIBUTION[4])
    
    # 11+ o'yinchilar uchun advanced
    roles = []
    
    # Mafiya soni: taxminan 30% (minimum 3)
    mafia_count = max(3, player_count // 3)
    roles.append("don")
    for i in range(mafia_count - 1):
        if i == 0:
            roles.append("advokat")
        elif i == 1:
            roles.append("yollanma_qotil")
        else:
            roles.append("mafia")
    
    # Asosiy tinch rollar
    roles.extend(["komissar", "serjant", "doctor", "daydi"])
    
    # Qo'shimcha faol rollar
    remaining = player_count - len(roles)
    
    if remaining >= 1:
        roles.append("kezuvchi")
        remaining -= 1
    if remaining >= 1:
        roles.append("fotparatchi")
        remaining -= 1
    if remaining >= 1:
        roles.append("robin_gud")
        remaining -= 1
    if remaining >= 1:
        roles.append("janob")
        remaining -= 1
    if remaining >= 1:
        roles.append("afsungar")
        remaining -= 1
    
    # Singleton (1-2 ta)
    if player_count >= 15 and remaining >= 1:
        roles.append("qotil")
        remaining -= 1
    if player_count >= 20 and remaining >= 1:
        roles.append("sehrgar")
        remaining -= 1
    
    # Qolganini tinch aholi bilan to'ldirish
    roles.extend(["citizen"] * remaining)
    
    return roles
