from flask import Flask, request
import subprocess
from threading import Thread

flask_app = Flask("")

@flask_app.route('/')
def home():
    return "Controller Active"

@flask_app.route('/run-bot', methods=['POST'])
def run_bot():
    Thread(target=lambda: subprocess.run(["python","bot_actual.py"])).start()
    return "Bot Started"

def run_flask():
    flask_app.run(host='0.0.0.0', port=8000)

Thread(target=run_flask).start()
print("Controller Flask server running...")