from exceptions import PrefixInvalid
from pymongo.errors import CollectionInvalid

from .db import bot_db

prefixes_coll = bot_db["prefixes"]
prefix_cache = {}
default_prefix_delimiter = ";"
default_prefixes = {
	"stable": "l" + default_prefix_delimiter,
	"indev": "r" + default_prefix_delimiter
}

def get_prefix(bot, message):
	server_id: int = message.guild.id
	bot_status = bot.status
	
	try:
		prefix = prefix_cache[server_id][bot_status]
	except KeyError:
		if not (prefix := find_prefix(server_id, bot_status)):
			prefix = insert_prefixes(server_id)[bot_status]
	
	return prefix + " ", prefix

def insert_prefixes(server_id, prefixes: dict=None):
	if not prefixes:
		prefixes_coll.insert_one({
			"_id": server_id,
			"prefixes": default_prefixes
		})
		
		return default_prefixes
	
	prefixes_coll.insert_one({
		"_id": server_id,
		"prefixes": prefixes
	})
	
	return prefixes

def find_prefix(server_id, bot_status):
	if server_data := prefixes_coll.find_one({"_id": server_id}):
		prefix = server_data["prefixes"][bot_status]
		prefix_cache[server_id] = prefix
		
		return prefix
	return None

def update_prefix(server_id, status, prefix):
	try:
		prefixes_coll.update_one({"_id": server_id}, {"prefixes": {status: prefix}})
		prefix_cache[server_id] = prefix
	except CollectionInvalid:
		# raise when stable and indev prefix are same
		raise PrefixInvalid(prefix)
