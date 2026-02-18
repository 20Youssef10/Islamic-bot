"""
Scheduled Azkar Service - Sends automatic azkar at specified times
"""

import discord
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from services.azkar_service import get_zikr
from db.database import get_connection

logger = logging.getLogger(__name__)

class ScheduledAzkarService:
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
    
    def start(self):
        """Start the scheduler"""
        # Schedule morning azkar (6:00 AM)
        self.scheduler.add_job(
            self.send_morning_azkar,
            CronTrigger(hour=6, minute=0),
            id='morning_azkar',
            replace_existing=True
        )
        
        # Schedule evening azkar (6:00 PM)
        self.scheduler.add_job(
            self.send_evening_azkar,
            CronTrigger(hour=18, minute=0),
            id='evening_azkar',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info("Azkar scheduler started")
    
    async def send_morning_azkar(self):
        """Send morning azkar to all configured channels"""
        await self._send_azkar_to_channels('morning', '🌅 أذكار الصباح')
    
    async def send_evening_azkar(self):
        """Send evening azkar to all configured channels"""
        await self._send_azkar_to_channels('evening', '🌙 أذكار المساء')
    
    async def _send_azkar_to_channels(self, azkar_type: str, title: str):
        """Send azkar to all configured channels"""
        try:
            channels = self._get_scheduled_channels(azkar_type)
            
            if not channels:
                logger.info(f"No channels configured for {azkar_type} azkar")
                return
            
            zikr = get_zikr(azkar_type)
            
            embed = discord.Embed(
                title=title,
                description=zikr,
                color=discord.Color.gold(),
                timestamp=datetime.now()
            )
            embed.set_footer(text="Islamic Bot - تذكير يومي")
            
            sent_count = 0
            for channel_id in channels:
                try:
                    channel = self.bot.get_channel(int(channel_id))
                    if channel:
                        await channel.send(embed=embed)
                        sent_count += 1
                        logger.info(f"Sent {azkar_type} azkar to channel {channel_id}")
                except Exception as e:
                    logger.error(f"Failed to send azkar to channel {channel_id}: {e}")
            
            logger.info(f"Sent {azkar_type} azkar to {sent_count} channels")
            
        except Exception as e:
            logger.error(f"Error sending {azkar_type} azkar: {e}", exc_info=True)
    
    def _get_scheduled_channels(self, schedule_type: str) -> list:
        """Get list of channel IDs configured for scheduled azkar"""
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT channel_id FROM scheduled_azkar WHERE schedule_type=? AND is_active=1",
                (schedule_type,)
            )
            rows = cur.fetchall()
            conn.close()
            return [row['channel_id'] for row in rows]
        except Exception as e:
            logger.error(f"Error getting scheduled channels: {e}")
            return []
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Azkar scheduler stopped")

async def setup_schedule_azkar_command(bot, interaction: discord.Interaction, schedule_type: str = None):
    """Command to configure scheduled azkar"""
    try:
        guild_id = str(interaction.guild_id)
        channel_id = str(interaction.channel_id)
        
        conn = get_connection()
        cur = conn.cursor()
        
        # Check if already configured
        cur.execute(
            "SELECT id FROM scheduled_azkar WHERE guild_id=? AND channel_id=? AND schedule_type=?",
            (guild_id, channel_id, schedule_type)
        )
        
        if cur.fetchone():
            # Toggle off
            cur.execute(
                "UPDATE scheduled_azkar SET is_active=0 WHERE guild_id=? AND channel_id=? AND schedule_type=?",
                (guild_id, channel_id, schedule_type)
            )
            conn.commit()
            conn.close()
            
            time_name = "الصباحية" if schedule_type == "morning" else "المسائية"
            await interaction.response.send_message(
                f"✅ تم إلغاء أذكار {time_name} في هذه القناة.",
                ephemeral=True
            )
        else:
            # Add new schedule
            schedule_time = "06:00" if schedule_type == "morning" else "18:00"
            cur.execute(
                "INSERT INTO scheduled_azkar (guild_id, channel_id, schedule_type, schedule_time, is_active) VALUES (?, ?, ?, ?, 1)",
                (guild_id, channel_id, schedule_type, schedule_time)
            )
            conn.commit()
            conn.close()
            
            time_name = "الصباحية (6:00 صباحاً)" if schedule_type == "morning" else "المسائية (6:00 مساءً)"
            await interaction.response.send_message(
                f"✅ تم تفعيل أذكار {time_name} في هذه القناة!",
                ephemeral=True
            )
        
    except Exception as e:
        logger.error(f"Error in schedule_azkar command: {e}")
        await interaction.response.send_message(
            "❌ حدث خطأ في إعداد الجدولة.",
            ephemeral=True
        )
