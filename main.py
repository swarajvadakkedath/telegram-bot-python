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

    # ---------- COMMANDS ----------

    @bot.message_handler(commands=["start", "hello"])
    def send_welcome(message):
        if not is_allowed(message):
            return
        bot.reply_to(
            message,
            "👋 Hi, I’m *Clawdbot*.\n\n"
            "I don’t agree by default.\n"
            "I challenge weak thinking and force trade-offs.\n\n"
            "Use /help to see commands or just talk.",
            parse_mode="Markdown",
        )

    @bot.message_handler(commands=["help"])
    def help_cmd(message):
        if not is_allowed(message):
            return
        bot.reply_to(
            message,
            "🛠 *Commands*\n\n"
            "/start – Welcome\n"
            "/help – This help\n"
            "/note <text> – Save a note\n"
            "/notes – Show notes\n"
            "/clear – Clear notes\n\n"
            "Or just send a message and I’ll challenge it.",
            parse_mode="Markdown",
        )

    @bot.message_handler(commands=["note"])
    def add_note(message):
        if not is_allowed(message):
            return
        text = message.text.replace("/note", "").strip()
        if not text:
            bot.reply_to(message, "Usage: /note <your note>")
            return
        notes.append(text)
        bot.reply_to(message, "✅ Note saved.")

    @bot.message_handler(commands=["notes"])
    def show_notes(message):
        if not is_allowed(message):
            return
        if not notes:
            bot.reply_to(message, "📭 No notes yet.")
            return
        msg = "📝 *Your Notes*\n\n"
        for i, n in enumerate(notes, 1):
            msg += f"{i}. {n}\n"
        bot.reply_to(message, msg, parse_mode="Markdown")

    @bot.message_handler(commands=["clear"])
    def clear_notes(message):
        if not is_allowed(message):
            return
        notes.clear()
        bot.reply_to(message, "🗑 Notes cleared.")

    # ---------- RULE-BASED CHAT ENGINE ----------

    @bot.message_handler(func=lambda msg: True)
    def chat(message):
        if not is_allowed(message):
            return

        text = message.text.lower()

        # Rule 1: vague / validation seeking
        if any(p in text for p in ["is this good", "is it good", "what do you think", "your opinion"]):
            bot.reply_to(
                message,
                "That question is vague.\n\n"
                "Good *for what*?\n"
                "• money\n"
                "• learning\n"
                "• speed\n"
                "• reputation\n\n"
                "Pick one. Otherwise the answer is meaningless."
            )
            return

        # Rule 2: redesign / overthinking
        if "redesign" in text or "again" in text:
            bot.reply_to(
                message,
                "Redesigning again is usually the wrong move.\n\n"
                "Most failures come from:\n"
                "• poor distribution\n"
                "• unclear messaging\n"
                "• weak content\n\n"
                "What *specific* problem are you trying to fix?"
            )
            return

        # Rule 3: perfectionism
        if any(p in text for p in ["perfect", "best possible", "ideal", "100%"]):
            bot.reply_to(
                message,
                "Perfectionism is not a strategy.\n\n"
                "It usually hides fear of shipping.\n"
                "What’s the deadline, and who defines ‘good enough’?"
            )
            return

        # Rule 4: tech choice
        if any(p in text for p in ["wordpress", "html", "react", "framework"]):
            bot.reply_to(
                message,
                "Tech choices are trade-offs, not preferences.\n\n"
                "WordPress → speed, iteration, hiring\n"
                "Custom code → control, performance, craftsmanship\n\n"
                "You can’t optimize both.\n"
                "Which matters *right now*?"
            )
            return

        # Rule 5: stuck / confused
        if any(p in text for p in ["confused", "stuck", "lost", "not sure"]):
            bot.reply_to(
                message,
                "Feeling stuck means too many options.\n\n"
                "What is the *next irreversible decision* you need to make?"
            )
            return

        # Default pushback
        bot.reply_to(
            message,
            "I won’t agree by default.\n\n"
            "State:\n"
            "• your goal\n"
            "• your constraint (time, money, skill)\n"
            "• what you’ve already tried\n\n"
            "Then I’ll give you a real answer."
        )

    # ---------- START BOT ----------

    bot.delete_webhook(drop_pending_updates=True)
    bot.polling()

except Exception as e:
    print(f"CRITICAL ERROR: Failed to initialize bot. Error: {e}")
    while True:
        time.sleep(3600)
