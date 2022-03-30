from tomli import load

from core.bot import LuxRay
from core.config import get_prefix, intent_generater
from utils.json_file import load_file

def get_loading_message() -> list:
	return load_file("loading_message.json")

def get_bot_config(config_path) -> dict:
	with open(config_path, "rb") as f:
		return load(f)

def setup_bot(config, mode):
	# Create Bot instance
	bot = LuxRay(command_prefix=get_prefix(config, mode), owner_id=config["misc"]["owner_ids"],
		intent=intent_generater(config, mode), config=config, mode=mode)
	
	return bot
