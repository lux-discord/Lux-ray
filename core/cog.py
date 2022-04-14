from disnake.ext.commands import Cog

from core.bot import LuxRay
from core.config import get_default_lang_code, get_default_prefix
from core.data import PrefixData, ServerData
from core.language import GLOBAL_DEFAULT_LANGUAGE, GeneralLanguage
from core.server import Server
from utils.token import Token


class GeneralCog(Cog):
	def __init__(self, bot: LuxRay) -> None:
		self.bot = bot
		self.token = Token
		
		# Shortcuts of db
		self.db = bot.db
		
		self.update_prefix = bot.db.update_prefix
		
		self.find_server = bot.db.find_server
		self.insert_server = bot.db.insert_server
		self.update_server = bot.db.update_server
	
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
			server_data = ServerData(_id=server_id, lang_code=get_default_lang_code(self.bot.config, self.bot.mode))
			await self.insert_server(server_data)
		
		return server_data
	
	async def get_server(self, server_id):
		return Server(await self.get_server_data(server_id))
