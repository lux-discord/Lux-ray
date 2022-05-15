from typing import TYPE_CHECKING

from motor.motor_asyncio import AsyncIOMotorClient

from core.data import PrefixData, ServerData

if TYPE_CHECKING:
    from typing import Optional

    from pymongo.database import Database
    from pymongo.results import DeleteResult, InsertOneResult, UpdateResult


class MongoDB:
    def __init__(self, host, *, port=None) -> None:
        self.client = AsyncIOMotorClient(host=host, port=port)
        self.bot_db: Database = self.client["discord-bot"]
        self.server = self.bot_db["server"]
        self.prefix = self.bot_db["prefix"]

    def __getitem__(self, name):
        return self.bot_db[name]

    # Prefix
    async def find_prefix(self, server_id: int) -> "Optional[str]":
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

    async def insert_prefix(self, prefix_data: PrefixData) -> "InsertOneResult":
        """
        Insert prefix

        Argument
        --------
        prefix: PrefixData
                prefix data

        Return type
        -----------
        pymongo.results.InsertOneResult
        """
        return await self.prefix.insert_one(prefix_data.to_dict())

    async def update_prefix(self, update: PrefixData) -> "UpdateResult":
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

    async def delete_prefix(self, server_id: int) -> "DeleteResult":
        """
        Delete prefix

        Argument
        --------
        server_id: `int`
                server id

        Return type
        -----------
        `pymongo.results.DeleteResult`
        """
        return await self.prefix.delete_one({"_id": server_id})

    # Server
    async def find_server(self, server_id: int) -> "Optional[dict]":
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

    async def insert_server(self, server_data: ServerData) -> "InsertOneResult":
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

    async def update_server(self, update: ServerData) -> "UpdateResult":
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

    async def delete_server(self, server_id: int) -> "DeleteResult":
        """
        Delete server data

        Argument
        --------
        server_id: `int`
                server id

        Return type
        -----------
        `pymongo.results.DeleteResult`
        """
        return await self.server.delete_one({"_id": server_id})
