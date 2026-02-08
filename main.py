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
        "👋 Hi, I’m <b>Clawdbot</b>.\n\n"
        "I’m here to help you think clearly, solve problems, "
        "and make better decisions — calmly and honestly.\n\n"
        "Ask me anything 🙂"
    )


@bot.message_handler(func=lambda m: True)
def companion_reply(message):
    text = message.text.strip().lower()

    # Simple conversational intelligence
    if text in ["hi", "hello", "hey"]:
        reply = "Hey 🙂 How can I help right now?"
    elif text.endswith("?"):
        reply = (
            "That’s a good question.\n\n"
            "Give me a second — I’ll walk you through it clearly."
        )
    else:
        reply = (
            "Got it.\n\n"
            "If you want, I can:\n"
            "• improve this\n"
            "• point out issues (only if there are any)\n"
            "• suggest a better approach"
        )

    bot.reply_to(message, reply)


bot.remove_webhook()
bot.infinity_polling(skip_pending=True)
