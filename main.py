import os
import time
import telebot
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN or OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode="HTML")
client = OpenAI(api_key=OPENAI_API_KEY)

# Claude-like personality
SYSTEM_PROMPT = """
You are Clawdbot, a calm, friendly, and thoughtful companion.

Behavior rules:
- Speak naturally, like a human
- Be warm and supportive
- Agree by default
- Correct only when the user is clearly wrong
- When correcting, be gentle and practical
- Do not argue
- Do not lecture
- Do not interrogate
- Keep answers concise but meaningful
"""

@bot.message_handler(commands=["start", "hello"])
def start(message):
    bot.reply_to(
        message,
        "👋 Hi! I’m <b>Clawdbot</b>.\n\n"
        "I’m here to help you think things through calmly.\n"
        "Ask me anything 🙂"
    )

@bot.message_handler(func=lambda msg: True)
def chat(message):
    try:
        user_text = message.text.strip()

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0.6,
            max_tokens=400
        )

        reply = response.choices[0].message.content
        bot.reply_to(message, reply)

    except Exception as e:
        print("AI ERROR:", e)
        bot.reply_to(
            message,
            "Sorry — I had a small hiccup. Can you try again?"
        )

# Start safely
try:
    bot.delete_webhook(drop_pending_updates=True)
    bot.polling(none_stop=True)

except Exception as e:
    print("CRITICAL ERROR:", e)
    while True:
        time.sleep(3600)
