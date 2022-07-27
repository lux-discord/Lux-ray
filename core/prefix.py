from typing import TYPE_CHECKING

from core.data import PrefixData
from core.exceptions import InvalidConfigValue

if TYPE_CHECKING:
    from disnake import Message

    from core.bot import LuxRay


async def get_prefix(bot: "LuxRay", message: "Message"):
    server_id = message.guild.id

    if not (prefix := await bot.db.find_prefix(server_id)):
        if default_prefix := bot.config.default_prefix:
            default_data = PrefixData(_id=server_id, prefix=default_prefix)
            await bot.db.insert_prefix(default_data)
            prefix = default_data.prefix
        else:
            raise InvalidConfigValue(f"prefix.{bot.config.mode}.prefix", "None")

    return prefix + " ", prefix
