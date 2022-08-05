from typing import TYPE_CHECKING

from motor.motor_asyncio import AsyncIOMotorClient

from core.data import ServerData, UserData
from core.database.base import BaseDriver, IdentiferData
from core.exceptions import DatabaseError

if TYPE_CHECKING:
    from typing import Optional

    from pymongo.database import Database


class MongoDriver(BaseDriver):
    def __init__(self, host, *, port=None) -> None:
        self.client = AsyncIOMotorClient(host=host, port=port)
        self.database: "Database" = self.client["discord-bot"]
        self.server = self.database["server"]
        self.user = self.database["user"]

    def __getitem__(self, name):
        return self.database[name]

    async def find(self, identifer_data: IdentiferData):
        collection = self.database.get_collection(identifer_data.category)
        return await collection.find(identifer_data.filter)

    async def insert(self, identifer_data: IdentiferData, *value):
        collection = self.database.get_collection(identifer_data.category)
        return await collection.insert_many(value)

    async def update(self, identifer_data: IdentiferData, value):
        collection = self.database.get_collection(identifer_data.category)
        update = {"$set": value}
        return await collection.update_many(identifer_data.filter, update)

    async def delete(self, identifer_data: IdentiferData):
        collection = self.database.get_collection(identifer_data.category)
        return await collection.delete_many(identifer_data.filter)

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
        except Exception as exc:
            raise DatabaseError("insert server") from exc

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
        except Exception as exc:
            raise DatabaseError("update server") from exc

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
        except Exception as exc:
            raise DatabaseError("delete server") from exc

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
        except Exception as exc:
            raise DatabaseError("insert user") from exc

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
        except Exception as exc:
            raise DatabaseError("update user") from exc

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
        except Exception as exc:
            raise DatabaseError("delete user") from exc
