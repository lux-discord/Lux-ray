from discord.ext.commands.cog import Cog
from core import InitedCog

class Event(InitedCog):
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.is_running:
			self.bot.is_running = True
			print("Bot is ready")
		else:
			print("Reconnected")

def setup(bot):
	bot.add_cog(Event(bot))

