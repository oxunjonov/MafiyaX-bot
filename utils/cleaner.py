from aiogram import Bot
from typing import List, Optional
import asyncio

class MessageCleaner:
    """
    Xabarlarni tracking va tozalash uchun
    Pro darajadagi message management
    """
    
    def __init__(self):
        # Guruh ID -> xabar ID lari
        self.tracked_messages = {}
    
    def track(self, chat_id: int, message_id: int):
        """Xabarni track qilish"""
        if chat_id not in self.tracked_messages:
            self.tracked_messages[chat_id] = []
        self.tracked_messages[chat_id].append(message_id)
    
    def track_multiple(self, chat_id: int, message_ids: List[int]):
        """Ko'p xabarlarni track qilish"""
        if chat_id not in self.tracked_messages:
            self.tracked_messages[chat_id] = []
        self.tracked_messages[chat_id].extend(message_ids)
    
    async def delete_tracked(self, bot: Bot, chat_id: int, keep_last: int = 0):
        """
        Track qilingan xabarlarni o'chirish
        keep_last: oxirgi N ta xabarni saqlash
        """
        if chat_id not in self.tracked_messages:
            return
        
        messages = self.tracked_messages[chat_id]
        
        # Oxirgi N ta xabarni saqlash
        if keep_last > 0:
            messages_to_delete = messages[:-keep_last]
        else:
            messages_to_delete = messages
        
        # Xabarlarni o'chirish (batch)
        for msg_id in messages_to_delete:
            try:
                await bot.delete_message(chat_id, msg_id)
                await asyncio.sleep(0.1)  # Anti-flood
            except:
                pass
        
        # Track listni yangilash
        if keep_last > 0:
            self.tracked_messages[chat_id] = messages[-keep_last:]
        else:
            self.tracked_messages[chat_id] = []
    
    async def delete_all(self, bot: Bot, chat_id: int):
        """Barcha track qilingan xabarlarni o'chirish"""
        await self.delete_tracked(bot, chat_id, keep_last=0)
    
    def clear_tracking(self, chat_id: int):
        """Track qilishni to'xtatish (o'chirmasdan)"""
        if chat_id in self.tracked_messages:
            self.tracked_messages[chat_id] = []
    
    def get_tracked_count(self, chat_id: int) -> int:
        """Track qilingan xabarlar soni"""
        if chat_id not in self.tracked_messages:
            return 0
        return len(self.tracked_messages[chat_id])

# Global instance
message_cleaner = MessageCleaner()
