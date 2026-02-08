import os
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

@bot.message_handler(commands=["start", "hello"])
def start(message):
    bot.reply_to(
        message,
        "👋 Hi, I’m <b>Clawdbot</b>.\n\n"
        "I’m here to help you think things through, "
        "stay organised, and make decisions calmly.\n\n"
        "What’s on your mind?"
    )

@bot.message_handler(func=lambda m: True)
def companion(message):
    text = message.text.strip().lower()

    # Greetings
    if text in ["hi", "hello", "hey", "yo"]:
        reply = "Hey 🙂 How can I help right now?"

    # Questions
    elif text.endswith("?"):
        reply = (
            "That’s a good question.\n\n"
            "Let’s look at it step by step. "
            "What part are you unsure about?"
        )

    # Confusion / uncertainty
    elif any(word in text for word in ["confused", "not sure", "stuck"]):
        reply = (
            "That happens 🙂\n\n"
            "Tell me what you’re trying to achieve, "
            "and we’ll simplify it."
        )

    # Statements / ideas
    else:
        reply = (
            "Got it.\n\n"
            "If you want, I can:\n"
            "• help you clarify this\n"
            "• point out possible issues\n"
            "• suggest a next step"
        )

    bot.reply_to(message, reply)

# Safety: polling only, no conflicts
bot.remove_webhook()
bot.infinity_polling(skip_pending=True)
