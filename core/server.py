from typing import TYPE_CHECKING

from core.data import ServerData
from core.language import GLOBAL_DEFAULT_LANGUAGE, get_language

if TYPE_CHECKING:
    from typing import Optional

    from utils.type_hint import EphemeralSendAble, SendAble


class Server:
    def __init__(self, server_data: ServerData) -> None:
        self.__items = server_data.items
        self.__id = server_data.id
        self.__lang_code = server_data.lang_code
        self.__role = server_data.role
        self.__channel = server_data.channel
        self.__message = server_data.message

        self.language = get_language(self.__lang_code)

    def __update_dict(self, target: dict[str], update: dict[str]):
        for key, value in update.items():
            if "." in key:
                main, sub = key.split(".", 1)
                target[main] = self.__update_dict(target.get(main, {}), {sub: value})
            else:
                target[key] = value
        return target

    def __update(self, updates: dict = None, **update):
        items = self.__items | update

        if updates:
            self.__update_dict(items, updates)

        return items

    def update(self, updates: dict = None, **update):
        items = self.__update(updates, **update)
        return self.__class__(ServerData.from_items(items))

    def Data(self, updates=None, **update):
        """
        Generate a `ServerData` instance with `update`

        Return
        ------
        A `ServerData` instance build with `self.items | update`

        Return type
        -----------
        `core.data.ServerData`
        """
        items = self.__update(updates, **update)
        return ServerData.from_items(items)

    def translate(self, message: str):
        """
        Argument
        --------
        message: str
                message that need translate

        Return
        ------
        The message that translated

        Return type
        -----------
        str
        """
        if self.__lang_code == GLOBAL_DEFAULT_LANGUAGE:
            return message

        return self.language.request_message(message)

    @property
    def id(self):
        return self.__id

    @property
    def lang_code(self):
        return self.__lang_code

    @property
    def role(self):
        return self.__role

    @property
    def channel(self):
        return self.__channel

    @property
    def message(self):
        return self.__message

    async def send(
        self, send_able: "SendAble", message: "Optional[str]" = None, **options
    ):
        message = self.translate(message) if message else None

        if message and (_format := options.pop("message_format", None)):
            message = message.format(**_format)

        return await send_able.send(message, **options)

    async def send_ephemeral(
        self,
        ephemeral_send_able: "EphemeralSendAble",
        message: "Optional[str]" = None,
        *,
        message_format: dict = None,
        **options,
    ):
        message = self.translate(message) if message else None

        if message and message_format:
            message = message.format(**message_format)

        return await ephemeral_send_able.send(message, ephemeral=True, **options)

    async def send_info(
        self, send_able: "SendAble", message: "Optional[str]" = None, **options
    ):
        return await self.send(send_able, message, delete_after=2, **options)

    async def send_warning(
        self, send_able: "SendAble", message: "Optional[str]" = None, **options
    ):
        return await self.send(send_able, message, delete_after=6, **options)

    async def send_error(
        self, send_able: "SendAble", message: "Optional[str]" = None, **options
    ):
        return await self.send(send_able, message, delete_after=10, **options)
