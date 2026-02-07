# DAY ENGINE
# Kun mexanikasi - Professional

import asyncio
from aiogram import Bot
from typing import Optional
from utils.voting_engine import VotingEngine
from utils.night_engine import NightResult
from utils.roles import ALL_ROLES

class DayEngine:
    """
    Professional Day Phase System
    
    Flow:
    1. Tun natijalari e'lon qilish
    2. Tirik o'yinchilar ro'yxati
    3. Ovoz berish (40 sek)
    4. Natija e'lon qilish
    5. Keyingi tun yoki g'alaba
    """
    
    def __init__(self, game, bot: Bot, chat_id: int):
        self.game = game
        self.bot = bot
        self.chat_id = chat_id
        self.voting: Optional[VotingEngine] = None
    
    async def start_day(self, night_result: NightResult, lang_data, day_number: int):
        """
        Kunni boshlash
        
        Args:
            night_result: Tun natijalari
            lang_data: Til ma'lumotlari
            day_number: Kun raqami
        """
        # GIF - Kun boshlandi
        day_gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDhsMnZiYzFyZGRxN2N4eXN5dGN4YnFyZjJvN2R3NWZqOGJ5cHprbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7btPCcdNniyf0ArS/giphy.gif"
        
        try:
            await self.bot.send_animation(
                self.chat_id,
                animation=day_gif_url,
                caption=f"☀️ **KUN {day_number}**"
            )
        except:
            # Agar GIF yuklanmasa
            await self.bot.send_message(
                self.chat_id,
                f"☀️ **KUN {day_number} BOSHLANDI**"
            )
        
        await asyncio.sleep(2)
        
        # Tun natijalari
        from utils.night_engine import NightEngine
        # Night Engine dan summary olish
        night_summary = self._get_night_summary(night_result)
        
        await self.bot.send_message(
            self.chat_id,
            night_summary,
            parse_mode="Markdown"
        )
        
        await asyncio.sleep(3)
        
        # Tirik o'yinchilar
        alive_text = self._get_alive_players_text()
        await self.bot.send_message(
            self.chat_id,
            alive_text,
            parse_mode="Markdown"
        )
        
        await asyncio.sleep(2)
        
        # G'alaba shartini tekshirish
        winner = self.game.check_win_condition()
        if winner:
            return winner
        
        # Ovoz berish boshlash
        await self._start_voting(lang_data)
        
        return None
    
    def _get_night_summary(self, night_result: NightResult) -> str:
        """Tun xulosasi"""
        if not night_result.deaths:
            return "✨ **Bu tunda hech kim o'lmadi!**\n\nShahar tinch uxladi... 😴"
        
        lines = ["💀 **BU TUNDA QUYIDAGILAR HALOK BO'LDI:**\n"]
        
        for player_id in night_result.deaths:
            player = self.game.get_player(player_id)
            if player:
                role_config = ALL_ROLES.get(player.role)
                role_name = role_config.name_uz if role_config else player.role
                role_emoji = role_config.emoji if role_config else "❓"
                
                # Mention
                if player.username:
                    mention = f"[@{player.username}](tg://user?id={player.user_id})"
                else:
                    mention = f"[{player.first_name}](tg://user?id={player.user_id})"
                
                lines.append(f"{role_emoji} {mention} - **{role_name}**")
        
        # Maxsus holatlar
        if night_result.afsungar_kills:
            lines.append("\n💣 **Afsungar o'ldi va o'ldirganini o'zi bilan olib ketdi!**")
        
        if night_result.bori_transform:
            lines.append("\n🐺 **Bo'ri transformatsiya bo'ldi!**")
        
        return "\n".join(lines)
    
    def _get_alive_players_text(self) -> str:
        """Tirik o'yinchilar ro'yxati"""
        alive = self.game.get_alive_players()
        
        lines = [f"👥 **TIRIK O'YINCHILAR: {len(alive)} ta**\n"]
        
        for i, player in enumerate(alive, 1):
            if player.username:
                mention = f"[@{player.username}](tg://user?id={player.user_id})"
            else:
                mention = f"[{player.first_name}](tg://user?id={player.user_id})"
            
            lines.append(f"{i}. {mention}")
        
        # Jamoa statistikasi
        citizens = len(self.game.get_players_by_team("citizen"))
        mafia = len(self.game.get_players_by_team("mafia"))
        singleton = len([p for p in alive if p.team == "singleton"])
        
        lines.append(f"\n📊 **Statistika:**")
        lines.append(f"🟢 Tinch: {citizens}")
        lines.append(f"🔴 Mafiya: {mafia}")
        if singleton > 0:
            lines.append(f"🟡 Yakka: {singleton}")
        
        return "\n".join(lines)
    
    async def _start_voting(self, lang_data):
        """Ovoz berishni boshlash"""
        alive = self.game.get_alive_players()
        candidate_ids = [p.user_id for p in alive]
        
        # Voting engine yaratish
        self.voting = VotingEngine(self.game, candidate_ids)
        
        # Ovoz berish xabari
        vote_text = f"""
🗳️ **OVOZ BERISH BOSHLANDI!**

⏰ Vaqt: **40 soniya**

Kimni osmoqchisiz? Pastdagi tugmalardan tanlang!

👍 - Taraf (osish uchun)
👎 - Qarshi (saqlab qolish uchun)
"""
        
        # Xabar yuborish va tracking
        vote_msg = await self.bot.send_message(
            self.chat_id,
            vote_text,
            parse_mode="Markdown"
        )
        
        # 40 soniya countdown
        for remaining in range(40, 0, -5):
            await asyncio.sleep(5)
            
            # Update xabar
            try:
                summary = self.voting.get_summary_text()
                updated_text = f"""
🗳️ **OVOZ BERISH**

⏰ Qoldi: **{remaining} soniya**

{summary}
"""
                keyboard = self.voting.get_voting_keyboard(0)  # Dummy voter_id
                
                await vote_msg.edit_text(
                    updated_text,
                    parse_mode="Markdown",
                    reply_markup=keyboard
                )
            except:
                pass
        
        # Natijalar
        await self._announce_voting_result(lang_data)
    
    async def _announce_voting_result(self, lang_data):
        """Ovoz berish natijasini e'lon qilish"""
        result = self.voting.get_results()
        
        if result.was_draw:
            await self.bot.send_message(
                self.chat_id,
                "⚖️ **DURRANG!**\n\nHech kim osilmadi. Ovozlar teng bo'lib qoldi."
            )
            return None
        
        if not result.hanged:
            await self.bot.send_message(
                self.chat_id,
                "❌ **HECH KIM OSILMADI!**\n\nYetarli ovoz to'planmadi."
            )
            return None
        
        # Osilgan odam
        hanged_player = self.game.get_player(result.hanged)
        if not hanged_player:
            return None
        
        # O'ldirish
        hanged_player.is_alive = False
        
        # E'lon qilish
        role_config = ALL_ROLES.get(hanged_player.role)
        role_name = role_config.name_uz if role_config else hanged_player.role
        role_emoji = role_config.emoji if role_config else "❓"
        
        if hanged_player.username:
            mention = f"[@{hanged_player.username}](tg://user?id={hanged_player.user_id})"
        else:
            mention = f"[{hanged_player.first_name}](tg://user?id={hanged_player.user_id})"
        
        await self.bot.send_message(
            self.chat_id,
            f"🪢 **OSILDI!**\n\n{role_emoji} {mention} - **{role_name}**",
            parse_mode="Markdown"
        )
        
        # Maxsus rol effektlari
        # Suitsid - darhol yutadi
        if hanged_player.role == "suitsid":
            await self.bot.send_message(
                self.chat_id,
                f"🤦 **SUITSID G'ALABA QILDI!**\n\n{mention} osildi va g'alaba qildi!",
                parse_mode="Markdown"
            )
            return "suitsid"
        
        # Afsungar - 1 kishini tanlaydi (keyingi versiya)
        
        return hanged_player.user_id
