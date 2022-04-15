from os import getenv

from disnake import Intents
from exceptions import DatabaseSettingNotFound, TokenNotFound
from utils.misc import import_from_path


def get_bot_token(mode: str) -> str:
	if not (token := getenv("BOT_TOKEN_ALL")):
		mode = mode.upper()
		
		if not (token := getenv(f"BOT_TOKEN_{mode}")):
			raise TokenNotFound(mode)
	
	return token

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

def get_default_prefix(config, mode):
	pconfig = config["prefix"][mode]
	return pconfig["prefix"]

def get_default_lang_code(config, mode):
	return config["server"]["default_lang_code"]

def get_db_client(mode: str):
	dbtype_to_class = {
		"mongodb": "core.db.MongoDB"
	}
	mode = mode.upper()
	
	if not (dbtype := getenv(key := f"DB_TYPE_{mode}")):
		raise DatabaseSettingNotFound(key)
	
	if not (db_host := getenv(key := f"DB_HOST_URI_{mode}")):
		raise DatabaseSettingNotFound(key)
	
	db_port = getenv(key := f"DB_HOST_PORT_{mode}")
	dbclass = import_from_path(dbtype_to_class[dbtype])
	client = dbclass(db_host=db_host, db_port=db_port)
	return client

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
