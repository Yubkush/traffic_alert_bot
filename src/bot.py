import os
from datetime import time
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, ContextTypes, JobQueue
import logging
from logging.handlers import RotatingFileHandler

from web_parser import get_tomorrows_game_data

TEST_MODE = False  # Set to True to enable test mode, False to disable

CHANNEL_ID = "@mtm_trafic_alert_channel"

load_dotenv()

# Configure logging with rotation
log_file = "bot.log"
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3),  # 5 MB max size, 3 backups
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def to_utc(hour: int):
    return hour - 2


async def send_games_daily(context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        text = get_tomorrows_game_data()
        if text:
            await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
    except Exception as e:
        logger.error("Error in send_games_daily: %s", e, exc_info=True)


async def send_startup_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a startup message to the channel in test mode."""
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text="Bot started in test mode.")
    except Exception as e:
        logger.error("Error in send_startup_message: %s", e, exc_info=True)

def main() -> None:
    try:
        """Run bot that sends game data"""
        app = ApplicationBuilder().token(os.getenv("TOKEN")).job_queue(JobQueue()).build()

        # Test mode: send a startup message
        if TEST_MODE:
            app.job_queue.run_once(send_startup_message, 0)

        app.job_queue.run_daily(send_games_daily, time(to_utc(21)))

        app.run_polling()
    except Exception as e:
        logger.critical("Critical error in main: %s", e, exc_info=True)


if __name__ == "__main__":
    main()
