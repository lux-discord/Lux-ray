import discord
from discord.ext.commands import Bot

from tools.prefix import load_prefixes, get_prefix
from tools.load import load_internal

from global_object import stable
from cog import cog_folders, cog_folder_loader

#prepare internal data
internal_data = load_internal()
token = internal_data["token"]
message = internal_data["message"]

#set up bot
print(message["set_up"])
load_prefixes()
intent = discord.Intents.all()
lrb = Bot(command_prefix = get_prefix, owner_id = internal_data["owner"], intents = intent)

#load cog
load_cog_message_keys = [
	"load_be",
	"load_cmd",
	"load_ext"
]

for folder, message_key in zip(cog_folders, load_cog_message_keys):
	print(message[message_key])
	cog_folder_loader(lrb, folder)

#start bot
print(message["start_bot"])
if stable:
	from keep_alive import keep_alive
	keep_alive()

lrb.run(token["main"] if stable else token["indev"])
