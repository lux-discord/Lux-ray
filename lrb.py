from discord import Intents

from core.cog import default_cog_folders, load_cog_folders
from core.prefix import get_prefix
from core.set_up import set_up_bot, get_loading_message, get_bot_config

lrb = set_up_bot(get_prefix, intent=Intents.all())
load_cog_folders(lrb, default_cog_folders, loading_messages=get_loading_message())

# import keep_alive if bot is stable
if lrb.stable:
	from keep_alive import keep_alive
	keep_alive()

bot_token = get_bot_config("token")
print("Starting bot")
lrb.run(bot_token)
