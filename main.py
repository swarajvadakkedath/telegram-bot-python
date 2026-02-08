import os
import telebot
from openai import OpenAI

# --- ENV ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_KEY:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN or OPENAI_API_KEY")

# --- CLIENTS ---
bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode="HTML")
client = OpenAI(api_key=OPENAI_KEY)

# --- MEMORY (simple, effective) ---
conversation_memory = {}

SYSTEM_PROMPT = """
You are Clawdbot.

Personality:
- calm, friendly, human-like
- supportive companion and online assistant
- do NOT argue
- do NOT lecture
- correct the user only if they are clearly wrong
- when correcting, be gentle and respectful
- offer better solutions as suggestions, not commands
- sound thoughtful, not robotic
- no emojis unless it feels natural

Tone:
- concise but warm
- like Claude web version
"""

MAX_HISTORY = 8  # per user


def get_reply(user_id: int, user_message: str) -> str:
    history = conversation_memory.get(user_id, [])

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.6,
    )

    assistant_reply = response.choices[0].message.content.strip()

    # update memory
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": assistant_reply})
    conversation_memory[user_id] = history[-MAX_HISTORY:]

    return assistant_reply


# --- HANDLERS ---

@bot.message_handler(commands=["start"])
def start(message):
    conversation_memory[message.from_user.id] = []
    bot.reply_to(
        message,
        "👋 Hi, I’m <b>Clawdbot</b>.\n\n"
        "I’m here to help you think, decide, and build — calmly and honestly.\n"
        "Ask me anything."
    )


@bot.message_handler(func=lambda m: True)
def chat(message):
    try:
        reply = get_reply(message.from_user.id, message.text)
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(
            message,
            "Something went wrong on my side.\n"
            "Try again in a moment."
        )
        print("ERROR:", e)


# --- START (IMPORTANT) ---
bot.remove_webhook()
bot.infinity_polling(skip_pending=True)
