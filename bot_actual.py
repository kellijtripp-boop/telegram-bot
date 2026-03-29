import os
import hashlib
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import threading
import time

TOKEN = os.environ.get("8667776112:AAFeJZ-jyCHqTVtTK7cQBWM2R6su8c1KSUY")
CHANNEL_ID = os.environ.get("@virallinkszone00") 

processed = set()
inactivity_seconds = 300  # 5 min inactivity → auto stop
last_activity = time.time()

def reset_timer():
    global last_activity
    last_activity = time.time()

def auto_stop_check():
    while True:
        time.sleep(10)
        if time.time() - last_activity > inactivity_seconds:
            print("No activity. Stopping bot...")
            exit()

threading.Thread(target=auto_stop_check, daemon=True).start()

def get_file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reset_timer()
    msg = update.message
    if msg.video:
        file = await msg.video.get_file()
        path = await file.download_to_drive()

        # Duplicate check
        file_hash = get_file_hash(path)
        if file_hash in processed:
            await msg.reply_text("⚠️ Already posted")
            return
        processed.add(file_hash)

        # Watermark
        clip = VideoFileClip(path)
        txt = TextClip("My Channel", fontsize=40, color='white')
        txt = txt.set_position(("center","bottom")).set_duration(clip.duration)

        final = CompositeVideoClip([clip, txt])
        output = "output.mp4"
        final.write_videofile(output, codec="libx264")

        # Send to channel
        await context.bot.send_video(
            chat_id=CHANNEL_ID,
            video=open(output, 'rb'),
            caption="🔥 New Video Uploaded\nJoin: https://t.me/your_channel"
        )

        os.remove(path)
        os.remove(output)

# Start bot
app_bot = ApplicationBuilder().token(TOKEN).build()
app_bot.add_handler(MessageHandler(filters.VIDEO, handle_video))
print("Main bot running...")
app_bot.run_polling()