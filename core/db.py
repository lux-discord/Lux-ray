from motor.motor_asyncio import AsyncIOMotorClient

from core.data import PrefixData, ServerData


class MongoDB():
	def __init__(self, db_host, *, db_port=None) -> None:
		self.client = AsyncIOMotorClient(host=db_host, port=db_port)
		self.bot_db = self.client["discord-bot"]
		self.server = self.bot_db["server"]
		self.prefix = self.bot_db["prefix"]
	
	# Prefix
	async def find_prefix(self, server_id: int):
		"""
		Find prefix by server id
		
		Argument
		--------
		server_id: int
			server id
		
		Return
		------
		The prefix of server or None if not found
		
		Return Type
		-----------
		Optinoal[str]
		"""
		doc = await self.prefix.find_one({"_id": server_id})
		return doc["prefix"] if doc else None
	
	async def insert_prefix(self, prefix_data: PrefixData):
		"""
		Insert prefix
		
		Argument
		--------
		prefix: PrefixData
			prefix data
		
		Return type
		-----------
		pumongo.results.InsertOneResult
		"""
		return await self.prefix.insert_one(prefix_data.to_dict())
	
	async def update_prefix(self, update: PrefixData):
		"""
		Update prefix
		
		Argument
		--------
		update: PrefixData
			new prefix data
		
		Return Type
		-----------
		pymongo.results.UpdateResult
		"""
		_update = {"$set": {"prefix": update.prefix}}
		return await self.prefix.update_one({"_id": update.id}, _update)
	
	# Server
	async def find_server(self, server_id: int):
		"""
		Find server by server id
		
		Argument
		--------
		server_id:
			server id
		
		Return
		------
		The server's data or None if not found
		
		Return type
		-----------
		Optinoal[dict]
		"""
		return await self.server.find_one({"_id": server_id})
	
	async def insert_server(self, server_data: ServerData):
		"""
		Argument
		--------
		server_id:
			server id
		
		server_data: ServerData
			server data
		
		Return type
		------
		pymongo.results.InsertOneResult
		"""
		return await self.server.insert_one(server_data.to_dict())
	
	async def update_server(self, update: ServerData):
		"""
		Update server
		
		Argument
		--------
		update: ServerData
			new server data
		
		Return type
		-----------
		pymongo.results.UpdateResult
		"""
		_update = {"$set": update.to_dict()}
		return await self.server.update_one({"_id": update.id}, _update)
