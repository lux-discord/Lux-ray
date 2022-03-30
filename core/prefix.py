from core.data import PrefixData
from core.config import get_default_prefix


async def get_prefix(bot, message):
	server_id = message.guild.id
	
	if not (prefix := await bot.db.find_prefix(server_id)):
		default_data = PrefixData(_id=server_id, prefix=get_default_prefix(bot.config, bot.mode))
		await bot.db.insert_prefix(default_data)
		prefix = default_data.prefix
	
	return prefix + " ", prefix
