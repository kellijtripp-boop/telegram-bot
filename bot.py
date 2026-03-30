import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from pytube import YouTube

TOKEN = "8667776112:AAFeJZ-jyCHqTVtTK7cQBWM2R6su8c1KSUY"
CHANNEL_ID = "@virallinkszone00"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a video link or forward a video!")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        file_path = stream.download()

        # ভিডিও চ্যানেলে পাঠানো
        await context.bot.send_video(chat_id=CHANNEL_ID, video=open(file_path, 'rb'))
        os.remove(file_path)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video))

    app.run_polling()

if __name__ == "__main__":
    main()
