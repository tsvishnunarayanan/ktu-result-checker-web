from flask import Flask
from threading import Thread
from bot import run_checker

app = Flask(__name__)

def background_task():
    run_checker()

@app.before_first_request
def start_bot():
    Thread(target=background_task).start()

@app.route('/')
def index():
    return "<h2>🎓 KTU Result Bot is Running in Background</h2><p>You'll get a Telegram alert when your result is out.</p>"

if __name__ == '__main__':
    app.run()
