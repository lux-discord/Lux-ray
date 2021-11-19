from typing import Union

from disnake.ext.commands import Bot, Cog
from core.language import request_language
from core.server import Server
from utils.token import Token

class InitedCog(Cog):
	def __init__(self, bot: Bot, *, lang_dir="language") -> None:
		# Basic attr
		self.bot = bot
		self.lang_dir = lang_dir
		
		# Shortcuts
		self.db = bot.db
		self.find_server = bot.db.find_server
		self.insert_server = bot.db.insert_server
		self.update_server = bot.db.update_server
	
	def get_message(self, server_id: int, token: Union[str, Token], **mes_format) -> str:
		"""
		Parameter
		---------
		server_id: int
			server's id
		token: utils.token.Token
			token that use to request message
		[lang_dir]="language": str
			language file's dirctory, default is public language dirctory
		[**mes_format]:
			use for format message
		
		Return type
		-----------
		str
		"""
		lang_code = self.get_server(server_id)["lang_code"]
		language = request_language(self.lang_dir, lang_code)
		
		if message := language.request_message(token) and mes_format:
			message = message.format(**mes_format)
		
		return message
	
	async def send_info(self, ctx, token: Union[str, Token], **mes_format):
		message = self.get_message(ctx.guild.id, token, **mes_format)
		return await ctx.send(message, delete_after=3)
	
	async def send_warning(self, ctx, token: Union[str, Token], **mes_format):
		message = self.get_message(ctx.guild.id, token, **mes_format)
		return await ctx.send(message, delete_after=6)
	
	async def send_error(self, ctx, token: Union[str, Token], **mes_format):
		message = self.get_message(ctx.guild.id, token, **mes_format)
		return await ctx.send(message, delete_after=9)
	
	def get_server(self, server_id):
		if server_data := self.db.get_server(server_id):
			return Server(server_data)
		return None
