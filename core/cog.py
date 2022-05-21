from typing import TYPE_CHECKING

from disnake.ext.commands import Cog

from core.bot import LuxRay
from core.data import PrefixData, ServerData
from core.language import GLOBAL_DEFAULT_LANGUAGE, get_language
from core.server import Server

if TYPE_CHECKING:
    from utils.type_hint import SendAble

server_cache: dict[int, Server] = {}


class GeneralCog(Cog):
    def __init__(self, bot: LuxRay) -> None:
        self.bot = bot
        self.db = bot.db

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

        language = get_language(lang_code)

        return language.request_message(message)

    async def _send(
        self, send_able: "SendAble", message: str, *, delete_after=None, **_format
    ):
        server_data = await self.get_server_data(send_able.guild.id)
        message = self.translate(server_data.lang_code, message)

        if _format:
            message = message.format(**_format)

        await send_able.send(message, delete_after=delete_after)

    async def send_info(self, send_able: "SendAble", message: str, **_format):
        return await self._send(send_able, message, delete_after=2, **_format)

    async def send_warning(self, send_able: "SendAble", message: str, **_format):
        return await self._send(send_able, message, delete_after=6, **_format)

    async def send_error(self, send_able: "SendAble", message: str, **_format):
        return await self._send(send_able, message, delete_after=2, **_format)

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
        if not (server := server_cache.get(server_id)):
            server = Server(await self.get_server_data(server_id))
            server_cache[server_id] = server

        return server

    async def find_server(self, server_id: int):
        return await self.db.find_server(server_id)

    async def insert_server(self, server_data: ServerData):
        await self.db.insert_server(server_data)

    async def update_server(self, update: ServerData):
        server_cache.pop(update.id, None)
        await self.db.update_server(update)
