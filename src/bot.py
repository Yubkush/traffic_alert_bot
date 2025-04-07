import os
from datetime import time
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, ContextTypes, JobQueue
import logging
from logging.handlers import RotatingFileHandler

from web_parser import get_tomorrows_game_data


GROUP_ID = "@mtm_trafic_alert_grp"

load_dotenv()

# Configure logging with rotation
log_file = "bot.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3),  # 5MB per file, 3 backups
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
            await context.bot.send_message(chat_id=GROUP_ID, text=text)
    except Exception as e:
        logger.error("Error in send_games_daily: %s", e, exc_info=True)


def main() -> None:
    try:
        """Run bot that sends game data"""
        app = ApplicationBuilder().token(os.getenv("TOKEN")).job_queue(JobQueue()).build()

        app.job_queue.run_daily(send_games_daily, time(to_utc(21)))

        app.run_polling()
    except Exception as e:
        logger.critical("Critical error in main: %s", e, exc_info=True)


if __name__ == "__main__":
    main()
