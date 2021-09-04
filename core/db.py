from pymongo import MongoClient

client = MongoClient()
bot_db = client["discord-bot"]
extension_server_db = client["discord-bot-extension"]

server_coll = bot_db["server"]
extension_coll = bot_db["extension"]
