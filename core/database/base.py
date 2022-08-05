from typing import TYPE_CHECKING

from core.data import IdBaseData

if TYPE_CHECKING:
    from typing import Optional

    from core.data import ServerData, UserData


class IdentiferData(IdBaseData):
    REQUIRE_ITEMS = ["category"]
    OPTIONAL_ITEMS = ["filter"]

    def __init__(self, **items) -> None:
        super().__init__(**items)
        self.category = items["category"]
        self.filter = items["filter"]


class BaseDriver:
    def __init__(self, *, host: str, port: int) -> None:
        raise NotImplementedError

    # Basic method
    async def find(self, identifer_data: IdentiferData):
        raise NotImplementedError

    async def insert(self, identifer_data: IdentiferData, value):
        raise NotImplementedError

    async def update(self, identifer_data: IdentiferData, value):
        raise NotImplementedError

    async def delete(self, identifer_data: IdentiferData):
        raise NotImplementedError

    # Server
    async def find_server(self, server_id: int) -> "Optional[dict]":
        raise NotImplementedError

    async def insert_server(self, server_data: "ServerData") -> "ServerData":
        raise NotImplementedError

    async def update_server(self, server_data: "ServerData") -> "ServerData":
        raise NotImplementedError

    async def delete_server(self, server_id: int) -> int:
        raise NotImplementedError

    # User
    async def find_user(self, user_id: int) -> "Optional[dict]":
        raise NotImplementedError

    async def insert_user(self, user_data: "UserData") -> "UserData":
        raise NotImplementedError

    async def update_user(self, user_data: "UserData") -> "UserData":
        raise NotImplementedError

    async def delete_user(self, user_id: int) -> int:
        raise NotImplementedError
