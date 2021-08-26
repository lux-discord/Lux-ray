from exceptions import PrefixInvalid, PrefixNotChange
from pymongo.errors import CollectionInvalid

from .db import bot_db

prefixes_coll = bot_db["prefixes"]
prefixes_cache = {}
default_prefix = {
	"stable": "l",
	"indev": "r"
}

def get_prefix(bot, message):
	server_id = message.guild.id
	
	try:
		prefix = prefixes_cache[server_id][bot.status]
	except KeyError:
		if not (prefixes := find_prefixes(server_id)):
			prefix = insert_prefixes(server_id)[bot.status]
		else:
			prefix = prefixes[bot.status]
	
	return prefix + ": "

def insert_prefixes(server_id, prefixes: dict=None):
	if prefixes:
		prefixes_cache[server_id] = prefixes
		prefixes_coll.insert_one({
			"server_id": server_id,
			"prefixes": prefixes
		})
	else:
		prefixes_cache[server_id] = default_prefix
		prefixes_coll.insert_one({
			"server_id": server_id,
			"prefixes": default_prefix
		})
	
	return prefixes_cache[server_id]

def find_prefixes(server_id):
	prefixes = prefixes_coll.find_one({"server_id": server_id})
	
	if prefixes:
		prefixes = prefixes["prefixes"]
		prefixes_cache[server_id] = prefixes
		
		return prefixes
	return None

def update_prefix(server_id, status, prefix):
	# won't happen KeyError, because this function must call by discord command that will add prefixes to cache
	if prefix == prefixes_cache[server_id][status]:
		raise PrefixNotChange
	
	try:
		prefixes_coll.update_one({"server_id": server_id}, {"prefixes": {status: prefix}})
		prefixes_cache[server_id][status] = prefix
	except CollectionInvalid:
		raise PrefixInvalid(prefix)
