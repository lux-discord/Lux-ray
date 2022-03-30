from motor.motor_asyncio import AsyncIOMotorClient



class MongoDB():
	def __init__(self, db_host, *, db_port=None) -> None:
		self.client = AsyncIOMotorClient(host=db_host, port=db_port)
		self.bot_db = self.client["discord-bot"]
		self.server = self.bot_db["server"]
		self.prefix = self.bot_db["prefix"]
	
	def _server_id_filter(self, server_id):
		"""
		Return a filter(dict) of server_id
		"""
		return {"_id": server_id}
	
	# Prefix
	def get_prefix(self, server_id: int):
		"""
		Alias of find_prefix
		"""
		return self.find_prefix(server_id)
	
	def find_prefix(self, server_id: int):
		"""
		Find prefix from db by server_id
		
		Argument
		--------
		server_id: int
			server ID
		
		Return
		------
		The server's prefix or None if not found
		
		Return Type
		-----------
		Optinoal[str]
		"""
		if doc := self.prefix.find_one(self._server_id_filter(server_id)):
			return doc["prefix"]
		
		return None
	
	def insert_prefix(self, server_id: int, prefix: str):
		"""
		Insert prefix by server id
		
		Argument
		--------
		server_id: int
			server id
		prefix: str
			server prefix
		
		Return
		------
		The prefix that pass in
		
		Return Type
		-----------
		str
		"""
		self.prefix.insert_one({
			"_id": server_id,
			"prefix": prefix,
		})
		
		return prefix
	
	def update_prefix(self, server_id: int, prefix: str):
		"""
		Update prefix by server ID
		
		Argument
		--------
		server_id: int
			server id
		prefix: str
			new server prefix
		
		Return
		------
		prefix that pass in
		
		Return Type
		-----------
		str
		"""
		self.prefix.update_one(
			filter=self._server_id_filter(server_id),
			update={"$set": {"prefix": prefix}}
		)
	
	# Server
	def get_server(self, server_id: int):
		"""
		Alias of find_server
		"""
		return self.find_server(server_id)
	
	def find_server(self, server_id: int):
		"""
		Unfinished...
		"""
		if doc := self.server.find_one(self._server_id_filter(server_id)):
			return doc
		
		return None
	
	def insert_server(self, server_id: int, server_data: dict=None):
		"""
		Unfinished...
		"""
		self.server.insert_one({
			"_id": server_id,
			"lang_code": "en"
		} if not server_data else server_data)
	
	def update_server(self, server_id: int, update: dict):
		"""
		Unfinished...
		
		TO DO:
		1. "update" use custom class instead
		"""
		self.server.update_one(
			filter=self._server_id_filter(server_id),
			update={"$set": update}
		)
