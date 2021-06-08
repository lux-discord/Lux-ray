from discord.ext.commands import Cog

__all__ = [
	"stable",
	"ready",
	"Inited_cog"
]

stable = False

def ready():
	global running
	running = False

class Inited_cog(Cog):
	def __init__(self, bot):
		self.bot = bot
