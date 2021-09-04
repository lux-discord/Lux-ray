from exceptions import PrefixInvalid, PrefixNotChange
from pymongo.errors import CollectionInvalid

from .db import bot_db

prefixes_coll = bot_db["prefixes"]
prefixes_cache = {}
default_prefix_delimiter = ";"
default_prefixes = {
	"stable": "l" + default_prefix_delimiter,
	"indev": "r" + default_prefix_delimiter
}

def get_prefix(bot, message):
	server_id: int = message.guild.id
	bot_status = bot.status
	
	try:
		prefix = prefixes_cache[server_id][bot_status]
	except KeyError:
		if not (prefix := find_prefix(server_id, bot_status)):
			prefix = insert_prefixes(server_id)[bot_status]
	
	return prefix + " ", prefix

def insert_prefixes(server_id, prefixes: dict=None):
	if not prefixes:
		prefixes_coll.insert_one({
			"server_id": server_id,
			"prefixes": default_prefixes
		})
		
		return default_prefixes
	
	prefixes_coll.insert_one({
		"server_id": server_id,
		"prefixes": prefixes
	})
	
	return prefixes

def find_prefix(server_id, bot_status):
	if server_data := prefixes_coll.find_one({"_id": server_id}):
		prefix = server_data["prefixes"][bot_status]
		prefix_cachees[server_id] = prefix
		
		return prefix
	return None

def update_prefix(server_id, status, prefix):
	try:
		prefixes_coll.update_one({"server_id": server_id}, {"prefixes": {status: prefix}})
		prefixes_cache[server_id][status] = prefix
	except CollectionInvalid:
		raise PrefixInvalid(prefix)
