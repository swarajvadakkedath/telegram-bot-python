import os
import time
import telebot
from dotenv import load_dotenv
from commands import register_commands

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# -----------------------------
# Bot personality (core behavior)
# -----------------------------
PERSONA = {
    "name": "Clawdbot",
    "style": "friendly",
    "role": "companion and online assistant"
}

try:
    bot = telebot.TeleBot(TOKEN)
    register_commands(bot)

    # -----------------------------
    # Start / Hello
    # -----------------------------
    @bot.message_handler(commands=["start", "hello"])
    def send_welcome(message):
        bot.reply_to(
            message,
            "👋 Hi! I’m *Clawdbot*.\n\n"
            "I’m here to help you think, decide, and build better.\n"
            "Ask anything — I’ll guide you naturally and correct you only when needed 🙂",
            parse_mode="Markdown"
        )

    # -----------------------------
    # Smart human-like message handler
    # -----------------------------
    @bot.message_handler(func=lambda msg: True)
    def smart_reply(message):
        text = message.text.strip()
        text_lower = text.lower()

        # --- Greetings ---
        if text_lower in ["hi", "hello", "hey", "yo", "hii"]:
            bot.reply_to(message, "Hey 🙂 What’s on your mind?")
            return

        # --- Capability question ---
        if "what can you do" in text_lower or "help me with" in text_lower:
            bot.reply_to(
                message,
                "I can help you:\n"
                "• think through problems\n"
                "• compare options\n"
                "• improve ideas\n"
                "• spot mistakes gently\n\n"
                "What are you working on right now?"
            )
            return

        # --- Decision / comparison ---
        if "should i" in text_lower or "which is better" in text_lower:
            bot.reply_to(
                message,
                "I can help 👍\n"
                "Tell me your goal and any limits you have (time, money, skill)."
            )
            return

        # --- Opinion seeking ---
        if "what do you think" in text_lower:
            bot.reply_to(
                message,
                "I’ll give you an honest take 🙂\n"
                "Share a bit more context so I don’t guess."
            )
            return

        # --- Default companion response ---
        bot.reply_to(
            message,
            "Got it 👍\n"
            "Tell me a little more so I can help properly."
        )

    # -----------------------------
    # Start polling
    # -----------------------------
    bot.delete_webhook(drop_pending_updates=True)
    bot.polling(none_stop=True)

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    print("Fix TELEGRAM_BOT_TOKEN and restart.")
    while True:
        time.sleep(3600)
