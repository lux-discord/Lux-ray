def get_prefix(bot, message):
	server_id = message.guild.id
	
	if not (prefix := bot.db.get_prefix(server_id)):
		prefix = bot.db.insert_prefix(server_id)
	
	return prefix + " ", prefix
