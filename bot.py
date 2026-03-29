from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8667776112:AAFeJZ-jyCHqTVtTK7cQBWM2R6su8c1KSUY"
CHANNEL_ID = "@virallinkszone00"

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if msg.video:
        file = await msg.video.get_file()
        path = await file.download_to_drive()

        await context.bot.send_video(
            chat_id=CHANNEL_ID,
            video=open(path, 'rb'),
            caption="🔥 New Video"
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.VIDEO, handle_video))
app.run_polling()