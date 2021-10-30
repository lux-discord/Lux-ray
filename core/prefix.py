prefix_cache = {}

def get_server_prefix(bot, message):
	"""
	Get prefix by server(guild) id
	
	get from cache, db or default value when both don't set
	"""
	server_id: int = message.guild.id
	
	try:
		prefix = prefix_cache[server_id]
	except KeyError:
		if not (prefix := bot.db.find_prefix(server_id=server_id)):
			# when bot enter a new server
			prefix = bot.db.insert_prefix(server_id=server_id)
	
	return prefix
