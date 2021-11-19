from disnake.ext.commands import Bot, Cog
from core.language import request_lang


class InitedCog(Cog):
	def __init__(self, bot: Bot) -> None:
		# Basic attr
		self.bot = bot
		
		# Shortcuts
		self.db = bot.db
		self.get_server = bot.db.get_server
		self.find_server = bot.db.find_server
		self.insert_server = bot.db.insert_server
		self.update_server = bot.db.update_server
	
	def get_message(self, server_id: int, token, *, lang_dir="language", **mes_format) -> str:
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
		language = request_lang(lang_dir, lang_code)
		
		if message := language.request_message(token) and mes_format:
			message = message.format(**mes_format)
		
		return message
	
	async def send_info(self, ctx, token, **mes_format):
		message = self.get_message(ctx.guild.id, token, **mes_format)
		return await ctx.send(message, delete_after=3)
	
	async def send_warning(self, ctx, token, **mes_format):
		message = self.get_message(ctx.guild.id, token, **mes_format)
		return await ctx.send(message, delete_after=6)
	
	async def send_error(self, ctx, token, **mes_format):
		message = self.get_message(ctx.guild.id, token, **mes_format)
		return await ctx.send(message, delete_after=9)

