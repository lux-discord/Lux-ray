from flask import Flask
from threading import Thread
from os import getenv

app = Flask('')

@app.route('/')
def main():
	return 'Bot is aLive!'

def run():
    app.run(host="0.0.0.0", port=getenv("PORT", 8080))

def keep_alive():
    server = Thread(target=run)
    server.start()
