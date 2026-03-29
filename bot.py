import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pytube import YouTube

TOKEN = "8667776112:AAFeJZ-jyCHqTVtTK7cQBWM2R6su8c1KSUY"
CHANNEL_ID = "@virallinkszone00"

def start(update, context):
    update.message.reply_text("Send me a video link or forward a video!")

def handle_video(update, context):
    url = update.message.text
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        file_path = stream.download()

        # ভিডিও চ্যানেলে পাঠানো
        context.bot.send_video(chat_id=CHANNEL_ID, video=open(file_path, 'rb'))
        os.remove(file_path)
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_video))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
