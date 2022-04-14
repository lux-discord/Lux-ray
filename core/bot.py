from disnake.ext.commands import Bot

from core.config import get_db_client


class LuxRay(Bot):
	def __init__(self, *args, config, mode, **kargs):
		self.db = get_db_client(config, mode)
		self.config = config
		self.mode = mode
		
		super().__init__(*args, **kargs)
