from disnake.ext.commands import Bot, Cog

class InitedCog(Cog):
	def __init__(self, bot: Bot) -> None:
		self.bot = bot
