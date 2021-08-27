from discord import Intents
from discord.ext.commands import Bot

from core.cog import cog_folder_loader, cog_folders
from core.prefix import get_prefix
from core.start_up import get_bot_data, load_start_up_message

# set up bot
start_up_message = load_start_up_message()
print(start_up_message["set_up"])
stable = True
status = "stable" if stable else "indev"
bot_data = get_bot_data(status)
intent = Intents.all()
lrb = Bot(command_prefix=get_prefix, owner_id=bot_data["owner"], intents=intent)
setattr(lrb, "status", status)
setattr(lrb, "is_running", False)

# load cog
load_cog_message_keys = [
	"load_be",
	"load_cmd",
	"load_ext"
]

for folder, message_key in zip(cog_folders, load_cog_message_keys):
	print(start_up_message[message_key])
	cog_folder_loader(lrb, folder)

# start bot
print(start_up_message["start_bot"])
if stable:
	from keep_alive import keep_alive
	keep_alive()

lrb.run(bot_data["token"])
