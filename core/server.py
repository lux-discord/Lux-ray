from core.data import ServerData
from core.language import GLOBAL_DEFAULT_LANGUAGE, GeneralLanguage


class Server:
    def __init__(self, server_data: ServerData) -> None:
        self._data = server_data
        self._items = server_data.items
        self._id = server_data.id
        self._lang_code = server_data.lang_code
        self._role = server_data.role
        self._role_member = server_data.role_member
        self._role_auto = server_data.role_auto
        self._keyword = server_data.keyword
        self._keyword_aliases = server_data.keyword_aliases
        self._keyword_replys = server_data.keyword_replys

    def update(self, **update):
        """
        Generate a `ServerData` instance with `update`

        Return
        ------
        A `ServerData` instance with `self.items | update`

        Return type
        -----------
        `core.data.ServerData`
        """
        new_items = self._items | update
        return ServerData.from_items(new_items)

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
    def lang_code(self):
        return self._lang_code

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
    def keyword_replys(self):
        return self._keyword_replys

    @property
    def keyword_aliases(self):
        return self._keyword_aliases

    async def _send(self, ctx, message: str, *, delete_after=None, **_format):
        message = self.translate(message)

        if _format:
            message = message.format(**_format)

        return await ctx.send(message, delete_after=delete_after)

    async def send_info(self, ctx, message: str, **_format):
        return await self._send(ctx, message, delete_after=2, **_format)

    async def send_warning(self, ctx, message: str, **_format):
        return await self._send(ctx, message, delete_after=6, **_format)

    async def send_error(self, ctx, message: str, **_format):
        return await self._send(ctx, message, delete_after=10, **_format)
