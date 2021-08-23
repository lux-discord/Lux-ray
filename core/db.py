from pymongo import MongoClient

client = MongoClient()
bot_db = client["discord-bot"]
