import os
from datetime import time
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, ContextTypes, JobQueue

from web_parser import get_week_game_data, get_next_day_game_data


GROUP_ID = "@mtm_trafic_alert_grp"

load_dotenv()


def to_utc(hour: int):
    return hour - 2


async def send_games_weekly(context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=GROUP_ID, text=get_week_game_data())


async def send_games_daily(context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=GROUP_ID, text=get_next_day_game_data())


def main() -> None:
    """Run bot that sends game data"""
    app = ApplicationBuilder().token(os.getenv("TOKEN")).job_queue(JobQueue()).build()

    app.job_queue.run_daily(send_games_weekly, time(to_utc(20)), days=(6,))

    app.job_queue.run_daily(send_games_daily, time(to_utc(21)), days=(0, 1, 2, 3, 6))

    app.run_polling()


if __name__ == "__main__":
    main()
