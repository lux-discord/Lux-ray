from pymongo import MongoClient

client = MongoClient()
bot_db = client["discord-bot"]
extension_server_db = client["bot-extension-server"]
