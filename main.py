import discord
import logging
import signal
import sys
import threading
import time
from bot.discord_client import IslamicBot
from db.models import init_db
from web_server import run_web_server, update_bot_status

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Global bot instance
bot = None

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    logger.info("Received shutdown signal, stopping bot...")
    if bot and hasattr(bot, 'scheduled_azkar') and bot.scheduled_azkar:
        bot.scheduled_azkar.stop()
    if bot and hasattr(bot, 'hourly_messages') and bot.hourly_messages:
        bot.hourly_messages.stop()
    update_bot_status("offline")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def update_web_status():
    """Update web dashboard with bot status periodically"""
    while True:
        try:
            if bot and bot.is_ready():
                update_bot_status(
                    status="online",
                    commands=88,  # Update this when adding new commands
                    guilds=len(bot.guilds)
                )
            else:
                update_bot_status("starting")
        except Exception as e:
            logger.error(f"Error updating web status: {e}")
        
        time.sleep(30)  # Update every 30 seconds

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("Starting Islamic Bot...")
    logger.info("=" * 50)
    
    # Start web server first (in background thread)
    logger.info("Starting web server for keep-alive...")
    run_web_server()
    update_bot_status("starting")
    
    # Give web server time to start
    time.sleep(2)
    
    # Initialize database
    logger.info("Initializing database...")
    init_db()
    logger.info("✓ Database initialized")
    
    # Start status updater thread
    status_thread = threading.Thread(target=update_web_status, daemon=True)
    status_thread.start()
    logger.info("✓ Status updater started")
    
    # Set up Discord intents
    intents = discord.Intents.default()
    intents.message_content = True  # Required for some features
    
    # Create bot instance
    logger.info("Creating bot instance...")
    bot = IslamicBot(intents=intents)
    
    try:
        logger.info("Starting bot...")
        logger.info("Web dashboard available at: http://0.0.0.0:10000")
        bot.run(bot.token)
    except Exception as e:
        logger.error(f"Error running bot: {e}", exc_info=True)
        update_bot_status("error")
        if bot and hasattr(bot, 'scheduled_azkar') and bot.scheduled_azkar:
            bot.scheduled_azkar.stop()
        if bot and hasattr(bot, 'hourly_messages') and bot.hourly_messages:
            bot.hourly_messages.stop()
        sys.exit(1)
