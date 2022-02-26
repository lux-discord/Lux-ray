from importlib import import_module

from disnake import Intents
from disnake.ext.commands import Bot
from tomli import load

from utils.json_file import load_file

def get_loading_message() -> list:
	return load_file("loading_message.json")

def get_bot_config(config_path) -> dict:
	with open(config_path, "rb") as f:
		return load(f)

def get_bot_token(config: dict, mode: str) -> dict:
	tokens = config["tokens"]
	return token if (token := tokens["all"]) else tokens[mode]

def import_from_path(import_path: str):
	module, name = import_path.rsplit(".", 1)
	return getattr(import_module(module), name)
		
def get_prefix(config, mode):
	pconfig = config["prefix"]
	ptype = pconfig["type"]
	pconfig = pconfig[mode]
	ptype_to_key = {
		"string": "prefix",
		"array": "prefixes",
	}
	
	if ptype == "function":
		prefix = import_from_path(pconfig["function_path"])
	else:
		prefix = pconfig[ptype_to_key[ptype]]
	
	return prefix

def get_db(config, mode):
	dbconfig = config["database"]
	dbtype = dbconfig["type"]
	dbconfig = dbconfig[mode]
	dbtype_to_class = {
		"mongodb": "core.db.MongoDB"
	}
	dbclass = import_from_path(dbtype_to_class[dbtype])
	db = dbclass(db_host=dbconfig["url"], db_port=port if (port := dbconfig["port"]) else None)
	return db

def intent_generater(config, mode):
	iconfig = config["intent"]
	base_type = iconfig["base"]
	intent_items = iconfig["items"]
	
	if base_type not in {"all", "default", "none"}:
		raise ValueError("Intent base type must be all, default or none")
	
	base_intent = getattr(Intents, base_type)()
	
	try:
		for item, value in intent_items.items():
			setattr(base_intent, item, value)
	except AttributeError:
		pass # raise InvalidIntentItem(f"Invalid intent item {item}")
	
	return base_intent

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
