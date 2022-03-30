from typing import Union

from disnake.ext.commands import Cog

from core.bot import LuxRay
from core.data import PrefixData, ServerData
from core.config import get_default_prefix, get_default_lang_code
from core.language import GeneralLanguage
from core.server import Server
from utils.token import Token


class GeneralCog(Cog):
	def __init__(self, bot: LuxRay) -> None:
		self.bot = bot
		self.token = Token
		
		# Shortcuts of db
		self.db = bot.db
		
		self.find_prefix = bot.db.find_prefix
		self.insert_prefix = bot.db.insert_prefix
		self.update_prefix = bot.db.update_prefix
		
		self.find_server = bot.db.find_server
		self.insert_server = bot.db.insert_server
		self.update_server = bot.db.update_server
	
	async def request_message(self, server_id: int, token: Token) -> str:
		"""
		Argument
		--------
		server_id: int
			server's id
		token: utils.token.Token
			token that use to request message
		
		Return
		------
		The message that request
		
		Return type
		-----------
		str
		"""
		server_data = await self.get_server_data(server_id)
		language = GeneralLanguage(server_data["lang_code"])
		
		return language.request_message(token)
	
	async def send_info(self, ctx, message: Union[str, Token], **format_):
		if isinstance(message, Token):
			message = await self.request_message(ctx.guild.id, message)
		
		if format_:
			message = message.format(**format_)
		
		return await ctx.send(message, delete_after=2)
	
	async def send_warning(self, ctx, message: Union[str, Token], **format_):
		if isinstance(message, Token):
			message = await self.request_message(ctx.guild.id, message)
		
		if format_:
			message = message.format(**format_)
		
		return await ctx.send(message, delete_after=6)
	
	async def send_error(self, ctx, message: Union[str, Token], **format_):
		if isinstance(message, Token):
			message = await self.request_message(ctx.guild.id, message)
		
		if format_:
			message = message.format(**format_)
		
		return await ctx.send(message, delete_after=10)
	
	async def get_prefix(self, server_id):
		"""
		Get prefix by server id
		
		Will auto create data if not found
		
		Argument
		--------
		server_id:
			server id
		
		Return
		------
		The prefix of server
		
		Return type
		-----------
		str
		"""
		if not (prefix := await self.find_prefix(server_id)):
			default_data = PrefixData(_id=server_id, prefix=get_default_prefix(self.bot.config, self.bot.mode))
			await self.insert_prefix(default_data)
			prefix = default_data.prefix
		
		return prefix
	
	async def get_server_data(self, server_id):
		"""
		Get server data by server id
		
		Will auto create data if not found
		
		Argument
		--------
		server_id: int
			server id
		
		Return
		------
		The server's data
		
		Return type
		-----------
		dict
		"""
		if not (server := await self.find_server(server_id)):
			default_data = ServerData(_id=server_id, lang_code=get_default_lang_code(self.bot.config, self.bot.mode))
			await self.insert_server(default_data)
			server = default_data.to_dict()
		
		return server
