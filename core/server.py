from typing import TYPE_CHECKING

from core.data import PrefixData, ServerData
from core.language import GLOBAL_DEFAULT_LANGUAGE, GeneralLanguage

if TYPE_CHECKING:
    from typing import Union

    from disnake import Interaction, SyncWebhook, Webhook
    from disnake.abc import Messageable

    SendAble = Union[Interaction, SyncWebhook, Webhook, Messageable]


class Server:
    def __init__(self, server_data: ServerData) -> None:
        self._data = server_data
        self._items = server_data.items
        self._id = server_data.id
        self._lang_code = server_data.lang_code
        self._listen_message = server_data.listen_message
        self._role = server_data.role
        self._role_member = server_data.role_member
        self._role_auto = server_data.role_auto
        self._keywords = server_data.keywords

    def update(self, **update):
        """
        Generate a `ServerData` instance with `update`

        Return
        ------
        A `ServerData` instance build with `self.items | update`

        Return type
        -----------
        `core.data.ServerData`
        """
        new_items = self._items | update
        return ServerData.from_items(new_items)

    def update_prefix(self, prefix: str):
        return PrefixData(_id=self._id, prefix=prefix)

    def translate(self, message):
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
        if self._lang_code == GLOBAL_DEFAULT_LANGUAGE:
            return message

        language = GeneralLanguage(self._lang_code)
        return language.request_message(message)

    @property
    def data(self):
        return self._data

    @property
    def id(self):
        return self._id

    @property
    def lang_code(self):
        return self._lang_code

    @property
    def listen_message(self):
        return self._listen_message

    @property
    def role(self):
        return self._role

    @property
    def role_member(self):
        return self._role_member

    @property
    def role_auto(self):
        return self._role_auto

    @property
    def keywords(self):
        return self._keywords

    async def _send(
        self, send_able: "SendAble", message: str, *, delete_after=None, **_format
    ):
        message = self.translate(message)

        if _format:
            message = message.format(**_format)

        return await send_able.send(message, delete_after=delete_after)

    async def send_info(self, send_able: "SendAble", message: str, **_format):
        return await self._send(send_able, message, delete_after=2, **_format)

    async def send_warning(self, send_able: "SendAble", message: str, **_format):
        return await self._send(send_able, message, delete_after=6, **_format)

    async def send_error(self, send_able: "SendAble", message: str, **_format):
        return await self._send(send_able, message, delete_after=10, **_format)
