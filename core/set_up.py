from json import load

from disnake.ext.commands import Bot

def get_loading_message() -> list:
	with open("loading_message.json", "r", encoding="UTF-8") as f:
		return load(f)

def get_bot_config(key=None, *, config_path=None):
	if not config_path:
		config_path = "bot-config.json"
	
	with open(config_path, "r", encoding="UTF-8") as f:
		bot_config: dict = load(f)
	
	status = "stable" if bot_config["stable"] else "indev"
	bot_config["token"] = bot_config["token"][status]
	bot_config["status"] = status
	
	if key:
		return bot_config.get(key)
	return bot_config

def set_up_bot(command_prefix, *, intent=None):
	bot_config = get_bot_config()
	
	print("Setting up bot")
	
	lrb = Bot(command_prefix=command_prefix, owner_id=bot_config.get("owner_id"), intent=intent)
	setattr(lrb, "stable", bot_config["stable"])
	setattr(lrb, "is_running", False) # for event on_ready judge is ready or reconnect
	return lrb
