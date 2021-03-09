from basic_import import *
from basic_cmd_import import *

class Task(Inited_cog):
	def __init__(self, *args, **kargs):
		super().__init__(*args, **kargs)
	
	async def morning():
		pass

def setup(bot):
	bot.add_cog(Task(bot))
