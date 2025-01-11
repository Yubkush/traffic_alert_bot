import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

def main() -> None:
    app = ApplicationBuilder().token(os.getenv('TOKEN')).build()

    app.add_handler(CommandHandler("hello", hello))

    app.run_polling()

if __name__ == "__main__":
    main()
