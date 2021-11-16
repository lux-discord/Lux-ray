from pymongo import MongoClient

class MongoDB():
	def __init__(self, db_host, *, db_port=None) -> None:
		self.client = MongoClient(host=db_host, port=db_port)
		self.bot_db = self.client["discord-bot"]
		self.server_coll = self.bot_db["server"]
		self.prefix_coll = self.bot_db["prefix"]
		self.prefix_cache = {}
		self.server_cache = {}
	
	def get_prefix(self, server_id: int):
		try:
			return self.prefix_cache[server_id]
		except KeyError:
			return self.find_prefix(server_id)
	
	def find_prefix(self, server_id: int):
		if prefix_doc := self.prefix_coll.find_one({"_id": server_id}):
			prefix = prefix_doc["prefix"]
			self.prefix_cache[server_id] = prefix
			return prefix
		
		return None
	
	def insert_prefix(self, server_id: int, *, prefix: str=None):
		"""
		Insert prefix to db by server id
		
		Argument
		--------
		server_id: int
			server's id
		prefix: str
			default "l;" if not pass in
		
		Return Type
		------
		prefix that pass in or default value
		"""
		prefix = prefix if prefix else "l;"
		self.prefix_coll.insert_one({
			"_id": server_id,
			"prefix": prefix,
		})
		self.prefix_cache[server_id] = prefix
		
		return prefix
	
	def update_prefix(self, server_id: int, prefix: str):
		self.prefix_coll.update_one(
			filter={"_id": server_id},
			update={"$set": {"prefix": prefix}}
		)
	
	def get_server(self, server_id: int):
		try:
			return self.server_cache[server_id]
		except KeyError:
			return self.find_server(server_id)
	
	def find_server(self, server_id: int):
		if server_doc := self.server_coll.find_one({"_id": server_id}):
			return server_doc
		
		return None
	
	def insert_server(self, server_id: int):
		pass
	
	def update_server(self, server_id: int, **kargs):
		pass

def get_prefix(bot, message):
	server_id = message.guild.id
	
	if not (prefix := bot.db.get_prefix(server_id)):
		prefix = bot.db.insert_prefix(server_id)
	
	return prefix
