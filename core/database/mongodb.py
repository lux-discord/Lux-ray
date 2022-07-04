from typing import TYPE_CHECKING

from motor.motor_asyncio import AsyncIOMotorClient

from core.data import PrefixData, ServerData, UserData
from core.exceptions import DatabaseError

if TYPE_CHECKING:
    from typing import Optional

    from pymongo.database import Database
    from pymongo.results import DeleteResult, InsertOneResult, UpdateResult


class MongoDriver:
    def __init__(self, host, *, port=None) -> None:
        self.client = AsyncIOMotorClient(host=host, port=port)
        self.bot_db: "Database" = self.client["discord-bot"]
        self.prefix = self.bot_db["prefix"]
        self.server = self.bot_db["server"]
        self.user = self.bot_db["user"]

    def __getitem__(self, name):
        return self.bot_db[name]

    # Prefix
    async def find_prefix(self, server_id: int) -> "Optional[str]":
        """
        Find prefix by server id

        Argument
        --------
        server_id: `int`
            server id

        Return
        ------
        The prefix of server or `None` if not found

        Return Type
        -----------
        `Optinoal[str]`
        """
        doc = await self.prefix.find_one(server_id)
        return doc["prefix"] if doc else None

    async def insert_prefix(self, prefix_data: PrefixData):
        """
        Insert prefix

        Argument
        --------
        prefix: `PrefixData`
            prefix data

        Return
        ------
        The `prefix_data` you passed in

        Return type
        -----------
        `core.data.PrefixData`
        """
        try:
            await self.prefix.insert_one(prefix_data.to_dict())
            return prefix_data
        except Exception:
            raise DatabaseError("insert prefix")

    async def update_prefix(self, update: PrefixData):
        """
        Update prefix

        Argument
        --------
        update: `PrefixData`
            new prefix data

        Return
        ------
        The `update` you passed in

        Return Type
        -----------
        `core.data.PrefixData`
        """
        try:
            _update = {"$set": {"prefix": update.prefix}}
            await self.prefix.update_one({"_id": update.id}, _update)
            return update
        except Exception:
            raise DatabaseError("update prefix")

    async def delete_prefix(self, server_id: int):
        """
        Delete prefix

        Argument
        --------
        server_id: `int`
            server id

        Return
        ------
        The `server_id` you passed in

        Return type
        -----------
        `int`
        """
        try:
            await self.prefix.delete_one({"_id": server_id})
            return server_id
        except Exception:
            raise DatabaseError("delete prefix")

    # Server
    async def find_server(self, server_id: int) -> "Optional[dict]":
        """
        Find server by server id

        Argument
        --------
        server_id: `int`
            server id

        Return
        ------
        A dictionary of server data or `None` if not found

        Return type
        -----------
        `Optinoal[dict]`
        """
        return await self.server.find_one(server_id)

    async def insert_server(self, server_data: ServerData):
        """
        Insert server

        Argument
        --------
        server_data: `ServerData`
            server data

        Return
        ------
        The `server_data` you passed in

        Return type
        ------
        `core.data.ServerData`
        """
        try:
            await self.server.insert_one(server_data.to_dict())
            return server_data
        except Exception:
            raise DatabaseError("insert server")

    async def update_server(self, update: ServerData):
        """
        Update server

        Argument
        --------
        update: `ServerData`
            new server data

        Return
        ------
        The `update` you passed in

        Return type
        -----------
        `core.data.ServerData`
        """
        try:
            _update = {"$set": update.to_dict()}
            await self.server.update_one({"_id": update.id}, _update)
            return update
        except Exception:
            raise DatabaseError("update server")

    async def delete_server(self, server_id: int):
        """
        Delete server

        Argument
        --------
        server_id: `int`
            server id

        Return
        ------
        The `server_id` you passed in

        Return type
        -----------
        `int`
        """
        try:
            await self.server.delete_one({"_id": server_id})
            return server_id
        except Exception:
            raise DatabaseError("delete server")

    # User
    async def find_user(self, user_id: int) -> "Optional[dict]":
        """
        Find user by user id

        Argument
        --------
        user_id: `int`
            user id

        Return
        ------
        A dictionary of user data or `None` if not found

        Return type
        -----------
        `Optional[dict]`
        """
        return await self.user.find_one(user_id)

    async def insert_user(self, user_data: UserData):
        """
        Insert user

        Argument
        --------
        user_data: `UserData`
            user data

        Return
        ------
        The `user_data` you passed in

        Return type
        -----------
        `core.data.UserData`
        """
        try:
            await self.user.insert_one(user_data.to_dict())
            return user_data
        except Exception:
            raise DatabaseError("insert user")

    async def update_user(self, update: UserData):
        """
        Update user

        Argument
        --------
        update: `UserData`
            new user data

        Return
        ------
        The `update` you passed in

        Return type
        -----------
        `core.data.UserData`
        """
        try:
            _update = {"$set": update.to_dict()}
            await self.user.update_one({"_id": update.id}, _update)
            return update
        except Exception:
            raise DatabaseError("update user")

    async def delete_user(self, user_id: int):
        """
        Delete user

        Argument
        --------
        user_id: `int`
            user id

        Return
        ------
        The `user_id` you passed in

        Return type
        -----------
        `int`
        """
        try:
            await self.user.delete_one({"_id": user_id})
            return user_id
        except Exception:
            raise DatabaseError("delete user")
