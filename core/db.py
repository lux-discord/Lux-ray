from functools import cache
from pymongo import MongoClient
from .server import Server

class MongoDB():
	def __init__(self, db_host, *, db_port=None) -> None:
		self.client = MongoClient(host=db_host, port=db_port)
		self.db = self.client["discord-bot"]
		self.server = self.db["server"]
		self.prefix = self.db["prefix"]
	
	@cache
	def get_prefix(self, server_id: int):
		return self.find_prefix(server_id)
	
	def find_prefix(self, server_id: int):
		if prefix_doc := self.prefix.find_one({"_id": server_id}):
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
		self.prefix.insert_one({
			"_id": server_id,
			"prefix": prefix,
		})
		self.prefix_cache[server_id] = prefix
		
		return prefix
	
	def update_prefix(self, server_id: int, prefix: str):
		self.prefix.update_one(
			filter={"_id": server_id},
			update={"$set": {"prefix": prefix}}
		)
	
	@cache
	def get_server(self, server_id: int):
		return self.find_server(server_id)
	
	def find_server(self, server_id: int):
		if server_doc := self.server.find_one({"_id": server_id}):
			return server_doc
		
		return None
	
	def insert_server(self, server_id: int):
		self.server.insert_one({
			"_id": server_id,
			"lang_code": "en"
		})
	
	def update_server(self, server_id: int, **kargs):
		self.server.update_one(
			filter={"_id": server_id},
			update={"$set": kargs}
		)

def get_prefix(bot, message):
	server_id = message.guild.id
	
	if not (prefix := bot.db.get_prefix(server_id)):
		prefix = bot.db.insert_prefix(server_id)
	
	return prefix
