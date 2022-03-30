from disnake import Intents

from utils.misc import import_from_path


def get_bot_token(config: dict, mode: str) -> dict:
	tokens = config["tokens"]
	return token if (token := tokens["all"]) else tokens[mode]

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

def get_db(config, mode):
	dbtype_to_class = {
		"mongodb": "core.db.MongoDB"
	}
	
	dbconfig = config["database"][mode]
	dbtype = dbconfig["type"]
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
