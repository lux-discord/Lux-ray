from disnake.ext.commands import Bot, Cog

from core.language import GLOBAL_LANGUAGE_DIR, GlobalLanguage
from core.server import Server
from utils.token import Token


class GeneralCog(Cog):
	def __init__(self, bot: Bot) -> None:
		self.bot = bot
		
		# Shortcuts
		## db
		self.db = bot.db
		self.get_server_data = bot.db.get_server
		self.find_server = bot.db.find_server
		self.insert_server = bot.db.insert_server
		self.update_server = bot.db.update_server
	
	def request_message(self, server_id: int, token: Token) -> str:
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
		lang_code = self.get_server_data(server_id)["lang_code"]
		language = GlobalLanguage(lang_code)
		
		return language.request_message(token)
	
	async def send_info(self, ctx, token: Token):
		message = self.request_message(ctx.guild.id, token)
		return await ctx.send(message, delete_after=2)
	
	async def send_warning(self, ctx, token: Token):
		message = self.request_message(ctx.guild.id, token)
		return await ctx.send(message, delete_after=6)
	
	async def send_error(self, ctx, token: Token):
		message = self.request_message(ctx.guild.id, token)
		return await ctx.send(message, delete_after=10)
	
	def get_server(self, server_id):
		if server_data := self.db.get_server(server_id):
			return Server(server_data)
		return None
	
	def token(self, string, *, delimiter=".") -> Token:
		return Token(string, delimiter=delimiter)
