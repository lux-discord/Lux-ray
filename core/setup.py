from disnake.ext.commands import Bot
from tomli import load

from utils.json_file import load_file

def get_loading_message() -> list:
	return load_file("loading_message.json")

def get_bot_config(config_path) -> dict:
	with open(config_path, "rb") as f:
		return load(f)

def setup_bot(config, mode):
	# Create Bot instance
	bot = Bot(command_prefix=get_prefix(config, mode), owner_id=config["misc"]["owner_ids"],
		intent=intent_generater(config, mode))
	
	# Set custom attr
	# Basic
	setattr(bot, "db", get_db(config, mode))
	setattr(bot, "config", config)
	# Additional
	setattr(bot, "mode", mode)
	# Deprecated
	setattr(bot, "is_running", False)
	
	return bot
