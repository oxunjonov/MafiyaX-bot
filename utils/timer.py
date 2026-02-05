import asyncio
from aiogram import Bot
from typing import Callable, Optional
from datetime import datetime, timedelta

class GameTimer:
    """
    Professional o'yin timer tizimi
    Countdown, notifications, callbacks
    """
    
    def __init__(self, bot: Bot, chat_id: int, duration: int, callback: Optional[Callable] = None):
        self.bot = bot
        self.chat_id = chat_id
        self.duration = duration  # soniyalarda
        self.callback = callback
        self.start_time = None
        self.end_time = None
        self.is_running = False
        self.is_paused = False
        self._task = None
        self.notification_message_id = None
    
    async def start(self):
        """Timer ni boshlash"""
        if self.is_running:
            return
        
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(seconds=self.duration)
        self.is_running = True
        self.is_paused = False
        
        # Timer task ni ishga tushirish
        self._task = asyncio.create_task(self._run_timer())
    
    async def _run_timer(self):
        """Timer asosiy jarayoni"""
        remaining = self.duration
        
        # Notification vaqtlari (5 min, 3 min, 1 min, 30 sec, 10 sec)
        notifications = {
            300: "⏰ O'yinga 5 daqiqa qoldi!",
            180: "⏰ O'yinga 3 daqiqa qoldi!",
            60: "⏰ O'yinga 1 daqiqa qoldi! Tezroq qo'shiling!",
            30: "⏰ 30 soniya qoldi!",
            10: "⏰ 10 soniya qoldi! 🚨"
        }
        
        while remaining > 0 and self.is_running:
            if not self.is_paused:
                # Notification yuborish
                if remaining in notifications:
                    try:
                        msg = await self.bot.send_message(
                            self.chat_id,
                            notifications[remaining]
                        )
                        # Eski notificationni o'chirish
                        if self.notification_message_id:
                            try:
                                await self.bot.delete_message(
                                    self.chat_id,
                                    self.notification_message_id
                                )
                            except:
                                pass
                        self.notification_message_id = msg.message_id
                    except:
                        pass
                
                await asyncio.sleep(1)
                remaining -= 1
            else:
                await asyncio.sleep(0.5)
        
        # Timer tugadi
        if self.is_running and remaining == 0:
            self.is_running = False
            if self.callback:
                await self.callback()
    
    async def pause(self):
        """Timer ni pauza qilish"""
        self.is_paused = True
    
    async def resume(self):
        """Timer ni davom ettirish"""
        self.is_paused = False
    
    async def stop(self):
        """Timer ni to'xtatish"""
        self.is_running = False
        if self._task:
            self._task.cancel()
    
    def get_remaining_time(self) -> int:
        """Qolgan vaqtni olish (soniyalarda)"""
        if not self.is_running or not self.end_time:
            return 0
        
        remaining = (self.end_time - datetime.now()).total_seconds()
        return max(0, int(remaining))
    
    def get_formatted_time(self) -> str:
        """Qolgan vaqtni formatlangan holda (MM:SS)"""
        remaining = self.get_remaining_time()
        minutes = remaining // 60
        seconds = remaining % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def get_progress_bar(self, length: int = 10) -> str:
        """Progress bar emoji bilan"""
        if not self.is_running:
            return "▱" * length
        
        remaining = self.get_remaining_time()
        progress = (self.duration - remaining) / self.duration
        filled = int(progress * length)
        
        bar = "▰" * filled + "▱" * (length - filled)
        return bar

class TimerManager:
    """Timer larni boshqarish uchun manager"""
    
    def __init__(self):
        self.timers = {}
    
    def create_timer(self, chat_id: int, bot: Bot, duration: int, callback: Optional[Callable] = None) -> GameTimer:
        """Yangi timer yaratish"""
        timer = GameTimer(bot, chat_id, duration, callback)
        self.timers[chat_id] = timer
        return timer
    
    def get_timer(self, chat_id: int) -> Optional[GameTimer]:
        """Timer ni olish"""
        return self.timers.get(chat_id)
    
    async def stop_timer(self, chat_id: int):
        """Timer ni to'xtatish va o'chirish"""
        if chat_id in self.timers:
            await self.timers[chat_id].stop()
            del self.timers[chat_id]
    
    def has_timer(self, chat_id: int) -> bool:
        """Timer bor ekanligini tekshirish"""
        return chat_id in self.timers and self.timers[chat_id].is_running

# Global instance
timer_manager = TimerManager()
