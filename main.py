import os
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "👋 Hi! I'm Clawdbot.\n\nI'm online and listening."
    )

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, message.text)

# VERY IMPORTANT: clear webhooks BEFORE polling
bot.remove_webhook()
bot.infinity_polling(skip_pending=True)
