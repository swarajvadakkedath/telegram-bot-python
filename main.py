import os
import time
import telebot
from dotenv import load_dotenv
from commands import register_commands

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID", "0"))

notes = []

try:
    bot = telebot.TeleBot(TOKEN)
    register_commands(bot)

    def is_allowed(message):
        return message.from_user and message.from_user.id == ALLOWED_USER_ID

    # ---------------- BASIC COMMANDS ----------------

    @bot.message_handler(commands=["start", "hello"])
    def start_bot(message):
        if not is_allowed(message):
            return

        bot.reply_to(
            message,
            "👋 Hi! I’m *Clawdbot*.\n\n"
            "I’m here to help you think, decide, and build better.\n"
            "Ask anything — I’ll guide you and gently correct you *only when needed* 🙂",
            parse_mode="Markdown",
        )

    @bot.message_handler(commands=["help"])
    def help_cmd(message):
        if not is_allowed(message):
            return

        bot.reply_to(
            message,
            "🛠 *What I can do*\n\n"
            "• Answer questions\n"
            "• Suggest better solutions\n"
            "• Point out mistakes (politely)\n"
            "• Help with decisions\n\n"
            "You can also save notes:\n"
            "/note <text>\n"
            "/notes\n"
            "/clear",
            parse_mode="Markdown",
        )

    # ---------------- NOTES ----------------

    @bot.message_handler(commands=["note"])
    def add_note(message):
        if not is_allowed(message):
            return

        text = message.text.replace("/note", "").strip()
        if not text:
            bot.reply_to(message, "Usage: /note <your note>")
            return

        notes.append(text)
        bot.reply_to(message, "✅ Noted.")

    @bot.message_handler(commands=["notes"])
    def show_notes(message):
        if not is_allowed(message):
            return

        if not notes:
            bot.reply_to(message, "You don’t have any notes yet.")
            return

        reply = "📝 *Your Notes*\n\n"
        for i, note in enumerate(notes, 1):
            reply += f"{i}. {note}\n"

        bot.reply_to(message, reply, parse_mode="Markdown")

    @bot.message_handler(commands=["clear"])
    def clear_notes(message):
        if not is_allowed(message):
            return

        notes.clear()
        bot.reply_to(message, "🗑 Notes cleared.")

    # ---------------- SMART CHAT ----------------

    @bot.message_handler(func=lambda msg: True)
    def assistant(message):
        if not is_allowed(message):
            return

        text = message.text.lower()

        # Friendly greetings
        if text in ["hi", "hello", "hey"]:
            bot.reply_to(message, "Hey 🙂 How can I help you today?")
            return

        # If user asks opinion
        if "what do you think" in text or "your opinion" in text:
            bot.reply_to(
                message,
                "I can share an opinion 👍\n\n"
                "Quick question first:\n"
                "What’s your goal here?"
            )
            return

        # If user sounds unsure
        if any(word in text for word in ["confused", "not sure", "stuck"]):
            bot.reply_to(
                message,
                "That’s okay — let’s break it down.\n\n"
                "What are you trying to achieve right now?"
            )
            return

        # Gentle correction (only when useful)
        if "perfect" in text or "best possible" in text:
            bot.reply_to(
                message,
                "Small note 🙂\n\n"
                "Chasing *perfect* can slow progress.\n"
                "Usually, *good + shipped* beats *perfect + late*.\n\n"
                "Want help defining a solid version?"
            )
            return

        # Tech-related guidance
        if any(word in text for word in ["wordpress", "custom", "react", "html"]):
            bot.reply_to(
                message,
                "Both approaches can work 👍\n\n"
                "A quick comparison:\n"
                "• WordPress → faster, easier updates\n"
                "• Custom code → more control, more effort\n\n"
                "What matters more to you right now?"
            )
            return

        # Default helpful response
        bot.reply_to(
            message,
            "Got it 👍\n\n"
            "Can you share a bit more detail so I can help better?"
        )

    # ---------------- START BOT ----------------

    bot.delete_webhook(drop_pending_updates=True)
    bot.polling()

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    while True:
        time.sleep(3600)
