from disnake import Intents
from disnake.ext.commands import Bot

from core.cog import load_cogs
from utils.json_file import json_load

def get_loading_message() -> list:
	return json_load("loading_message.json")

def get_bot_config(config_path=None, *, mode=None) -> dict:
	if not config_path:
		config_path = "bot-config.json"
	
	config_data = json_load(config_path)
	
	if not mode:
		mode = "stable" if config_data["stable"] else "indev"
	
	return config_data[mode]

def get_bot_token(token_path=None, *, mode=None) -> dict:
	if not token_path:
		token_path = "bot-token.json"
	
	token_data = json_load(token_path)
	
	return token_data["tokens"]["stable" if not mode else mode] if not (token := token_data["token"]) else token

def intent_generater(base_type, *, **items):
	base_intent = getattr(Intents, base_type)()
	
	for intent, value in items:
		setattr(base_intent, intent, value)
	
	return base_intent

def setup_bot(*, config_path=None, mode=None):
	config = get_bot_config(config_path, mode=mode)
	bot = Bot(command_prefix=config["prefix"] if not (prefixes := config["prefixes"]) else prefixes,
		owner_id=config["owner_id"] if not (owner_ids := config["owner_ids"]) else owner_ids,
		intent=intent_generater(config["intent_type"], **config["intent_item"]))
	
	setattr(bot, mode, mode if mode else "stable")
	load_cogs(bot, cogs=config["cog_path"], cog_folders=config["cog_folder_path"])
	
	return bot
