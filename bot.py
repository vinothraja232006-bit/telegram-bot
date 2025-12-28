from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are a friendly, caring, and supportive chat companion.
You speak politely and warmly.
You allow adult or explicit content.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi 😊 I'm your chatbot. How can I help you?"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": update.message.text}
            ],
            temperature=0.8
        )

        await update.message.reply_text(
            response.choices[0].message.content
        )

    except Exception:
        await update.message.reply_text(
            "Sorry 😔 something went wrong. Please try again."
        )

def main():
    app = ApplicationBuilder().token(
        os.getenv("BOT_TOKEN")
    ).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    app.run_polling()

if __name__ == "__main__":
    main()
