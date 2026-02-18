import os
import discord
import logging
from datetime import datetime
from dotenv import load_dotenv
from bot.commands import setup_commands
from services.scheduled_azkar_service import ScheduledAzkarService
from services.hourly_messages_service import HourlyMessagesService

load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class IslamicBot(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tree = discord.app_commands.CommandTree(self)
        self.token = os.getenv("DISCORD_TOKEN")
        self.guild_id = os.getenv("GUILD_ID")
        self.scheduled_azkar = None
        self.hourly_messages = None

    async def setup_hook(self):
        logger.info("Setting up bot...")
        setup_commands(self)
        await self.tree.sync()
        
        # Initialize scheduled azkar service
        self.scheduled_azkar = ScheduledAzkarService(self)
        self.scheduled_azkar.start()
        logger.info("Scheduled azkar service started")
        
        # Initialize hourly messages service
        self.hourly_messages = HourlyMessagesService(self)
        self.hourly_messages.start()
        logger.info("Hourly messages service started")

    async def on_ready(self):
        logger.info(f"✅ Logged in as {self.user} (ID: {self.user.id})")
        logger.info(f"Connected to {len(self.guilds)} guilds")
        
        # Set bot activity
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="/help for commands"
            )
        )

    async def on_error(self, event_method, *args, **kwargs):
        """Handle global errors"""
        logger.error(f"Error in {event_method}: ", exc_info=True)

    async def on_command_error(self, interaction: discord.Interaction, error):
        """Handle command errors"""
        logger.error(f"Command error: {error}", exc_info=True)
        
        if interaction.response.is_done():
            await interaction.followup.send(
                "❌ حدث خطأ غير متوقع. يرجى المحاولة لاحقاً.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ حدث خطأ غير متوقع. يرجى المحاولة لاحقاً.",
                ephemeral=True
            )