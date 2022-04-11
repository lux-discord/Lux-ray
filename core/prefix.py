from core.config import get_default_prefix
from core.data import PrefixData
from exceptions import ConfigInvalid


async def get_prefix(bot, message):
	server_id = message.guild.id
	
	if not (prefix := await bot.db.find_prefix(server_id)):
		if default_prefix := get_default_prefix(bot.config, bot.mode):
			default_data = PrefixData(_id=server_id, prefix=default_prefix)
			await bot.db.insert_prefix(default_data)
			prefix = default_data.prefix
		else:
			raise ConfigInvalid(f"prefix.{bot.mode}.prefix", "None")
	
	return prefix + " ", prefix
