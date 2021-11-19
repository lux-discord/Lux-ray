from disnake.ext.commands import Bot, Cog

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
