from disnake import Intents
from disnake.ext.commands import Bot

from utils.json_file import load_file

def get_loading_message() -> list:
	return load_file("loading_message.json")

def get_bot_config(config_path, mode) -> dict:
	config_data = load_file(config_path)
	return config_data[mode]

def get_bot_token(token_path, mode) -> dict:
	token_data = load_file(token_path)
	return token_data["tokens"][mode] if not (token := token_data["token"]) else token

def intent_generater(base_type, **items):
	base_intent = getattr(Intents, base_type)()
	
	for intent, value in items:
		setattr(base_intent, intent, value)
	
	return base_intent

def setup_bot(config, mode, db):
	# Set prefix
	if not (prefix := config["prefix"]):
		# If not set prefix, get it from db
		prefix = db.get_prefix
	
	# Create Bot instance
	bot = Bot(command_prefix=prefix,
		owner_id=config["owner_id"] if not (owner_ids := config["owner_ids"]) else owner_ids,
		intent=intent_generater(config["intent_type"], **config["intent_item"]))
	
	# Add custom attr
	setattr(bot, "db", db)
	setattr(bot, "config", config)
	setattr(bot, "mode", mode)
	
	return bot
