from disnake.ext.commands import Cog

from core.bot import LuxRay
from core.data import PrefixData, ServerData
from core.language import GLOBAL_DEFAULT_LANGUAGE, GeneralLanguage
from core.server import Server


class GeneralCog(Cog):
    def __init__(self, bot: LuxRay) -> None:
        self.bot = bot
        self.db = bot.db
        self.__server_cache = {}

    @staticmethod
    def translate(lang_code: str, message: str) -> str:
        """
        Argument
        --------
        guild_id: int
                the guidl's id
        message: str
                the message that need translate

        Return
        ------
        The message that translated

        Return type
        -----------
        str
        """
        if lang_code == GLOBAL_DEFAULT_LANGUAGE:
            return message

        language = GeneralLanguage(lang_code)

        return language.request_message(message)

    async def _send(self, ctx, message: str, *, delete_after=None, **_format):
        server_data = await self.get_server_data(ctx.guild.id)
        message = self.translate(server_data.lang_code, message)

        if _format:
            message = message.format(**_format)

        await ctx.send(message, delete_after=delete_after)

    async def send_info(self, ctx, message: str, **_format):
        return await self._send(ctx, message, delete_after=2, **_format)

    async def send_warning(self, ctx, message: str, **_format):
        return await self._send(ctx, message, delete_after=6, **_format)

    async def send_error(self, ctx, message: str, **_format):
        return await self._send(ctx, message, delete_after=2, **_format)

    async def update_prefix(self, update: PrefixData):
        await self.db.update_prefix(update)

    async def get_server_data(self, server_id):
        """
        Get server data by server id

        Will auto create data if not found

        Argument
        --------
        server_id: `int`
                server id

        Return
        ------
        The server's data

        Return type
        -----------
        `core.data.ServerData`
        """
        if raw_server_data := await self.find_server(server_id):
            server_data = ServerData(**raw_server_data)
        else:
            server_data = ServerData(
                _id=server_id,
                lang_code=self.bot.config.default_lang_code,
            )
            await self.insert_server(server_data)

        return server_data

    async def get_server(self, server_id):
        if not (server := self.__server_cache.get(server_id)):
            server = Server(await self.get_server_data(server_id))
            self.__server_cache[server_id] = server

        return server

    async def find_server(self, server_id: int):
        return await self.db.find_server(server_id)

    async def insert_server(self, server_data: ServerData):
        await self.db.insert_server(server_data)

    async def update_server(self, update: ServerData):
        await self.db.update_server(update)
        self.__server_cache.pop(update.id, None)
