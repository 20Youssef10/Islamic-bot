"""
Hourly Random Messages Service - Sends random Islamic content every hour
"""

import discord
import random
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from services.quran_service import get_random_ayah
from services.azkar_service import get_zikr
from services.hadith_service import get_random_hadith
from services.islamic_knowledge_service import get_dua
from db.database import get_connection

logger = logging.getLogger(__name__)

class HourlyMessagesService:
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.message_types = ["dua", "dhikr", "hadith", "ayah"]
    
    def start(self):
        """Start the hourly scheduler"""
        # Schedule to run every hour
        self.scheduler.add_job(
            self.send_hourly_message,
            IntervalTrigger(hours=1),
            id='hourly_islamic_messages',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info("Hourly Islamic messages scheduler started")
    
    async def send_hourly_message(self):
        """Send random Islamic message to all configured channels"""
        try:
            channels = self._get_hourly_message_channels()
            
            if not channels:
                logger.info("No channels configured for hourly messages")
                return
            
            # Select random message type
            message_type = random.choice(self.message_types)
            
            # Generate message based on type
            embed = await self._generate_message(message_type)
            
            if not embed:
                logger.error(f"Failed to generate message for type: {message_type}")
                return
            
            sent_count = 0
            for channel_id in channels:
                try:
                    channel = self.bot.get_channel(int(channel_id))
                    if channel:
                        await channel.send(embed=embed)
                        sent_count += 1
                        logger.info(f"Sent hourly {message_type} message to channel {channel_id}")
                    else:
                        logger.warning(f"Channel {channel_id} not found or bot cannot access it")
                except Exception as e:
                    logger.error(f"Failed to send message to channel {channel_id}: {e}")
            
            logger.info(f"Sent hourly message to {sent_count} channels")
            
        except Exception as e:
            logger.error(f"Error sending hourly message: {e}", exc_info=True)
    
    async def _generate_message(self, message_type: str):
        """Generate embed message based on type"""
        try:
            if message_type == "dua":
                dua_data = get_dua()
                embed = discord.Embed(
                    title="🤲 دعاء",
                    description=dua_data['dua'],
                    color=discord.Color.green(),
                    timestamp=datetime.now()
                )
                embed.add_field(name="الحالة", value=dua_data['situation'], inline=True)
                if 'translation' in dua_data:
                    embed.add_field(name="الترجمة", value=dua_data['translation'], inline=False)
                embed.set_footer(text="رسالة ساعية - دعاء")
                return embed
            
            elif message_type == "dhikr":
                # Get random dhikr type
                dhikr_type = random.choice(["morning", "evening"])
                zikr = get_zikr(dhikr_type)
                time_name = "أذكار الصباح" if dhikr_type == "morning" else "أذكار المساء"
                emoji = "🌅" if dhikr_type == "morning" else "🌙"
                
                embed = discord.Embed(
                    title=f"{emoji} {time_name}",
                    description=zikr,
                    color=discord.Color.gold(),
                    timestamp=datetime.now()
                )
                embed.set_footer(text="رسالة ساعية - ذكر")
                return embed
            
            elif message_type == "hadith":
                hadith_data = get_random_hadith()
                
                if "error" in hadith_data:
                    return None
                
                embed = discord.Embed(
                    title=f"📚 {hadith_data['collection']}",
                    description=hadith_data['text'],
                    color=discord.Color.orange(),
                    timestamp=datetime.now()
                )
                embed.add_field(name="الراوي", value=hadith_data.get('narrator', 'غير معروف'), inline=True)
                embed.set_footer(text="رسالة ساعية - حديث")
                return embed
            
            elif message_type == "ayah":
                ayah_data = get_random_ayah()
                
                embed = discord.Embed(
                    title=f"📖 {ayah_data['ref']}",
                    description=ayah_data['text'],
                    color=discord.Color.teal(),
                    timestamp=datetime.now()
                )
                embed.set_footer(text="رسالة ساعية - آية قرآنية")
                return embed
            
            return None
            
        except Exception as e:
            logger.error(f"Error generating message: {e}")
            return None
    
    def _get_hourly_message_channels(self) -> list:
        """Get list of channel IDs configured for hourly messages"""
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT channel_id FROM scheduled_azkar WHERE schedule_type='hourly_messages' AND is_active=1"
            )
            rows = cur.fetchall()
            conn.close()
            return [row['channel_id'] for row in rows]
        except Exception as e:
            logger.error(f"Error getting hourly message channels: {e}")
            return []
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Hourly messages scheduler stopped")

async def setup_hourly_messages_command(bot, interaction: discord.Interaction):
    """Command to configure hourly messages"""
    try:
        guild_id = str(interaction.guild_id)
        channel_id = str(interaction.channel_id)
        
        conn = get_connection()
        cur = conn.cursor()
        
        # Check if already configured
        cur.execute(
            "SELECT id FROM scheduled_azkar WHERE guild_id=? AND channel_id=? AND schedule_type='hourly_messages'",
            (guild_id, channel_id)
        )
        
        if cur.fetchone():
            # Toggle off
            cur.execute(
                "DELETE FROM scheduled_azkar WHERE guild_id=? AND channel_id=? AND schedule_type='hourly_messages'",
                (guild_id, channel_id)
            )
            conn.commit()
            conn.close()
            await interaction.response.send_message(
                "✅ تم إلغاء الرسائل الساعية في هذه القناة.",
                ephemeral=True
            )
        else:
            # Add new schedule
            cur.execute(
                "INSERT INTO scheduled_azkar (guild_id, channel_id, schedule_type, schedule_time, is_active) VALUES (?, ?, 'hourly_messages', '00:00', 1)",
                (guild_id, channel_id)
            )
            conn.commit()
            conn.close()
            
            await interaction.response.send_message(
                "✅ تم تفعيل الرسائل الساعية في هذه القناة!\n\n"
                "سيتم إرسال رسالة عشوائية كل ساعة:\n"
                "• دعاء\n"
                "• ذكر\n"
                "• حديث\n"
                "• آية قرآنية",
                ephemeral=True
            )
        
    except Exception as e:
        logger.error(f"Error in setup_hourly_messages command: {e}")
        await interaction.response.send_message(
            "❌ حدث خطأ في الإعداد.",
            ephemeral=True
        )
