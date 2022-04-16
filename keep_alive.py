from os import getenv
from threading import Thread

from flask import Flask

app = Flask("")


@app.route("/")
def main():
    return "Bot is aLive!"


def run():
    app.run(host="0.0.0.0", port=getenv("PORT", 8080))


def keep_alive():
    server = Thread(target=run)
    server.start()
