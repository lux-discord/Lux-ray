from sys import argv
from pathlib import Path

from click import group, prompt, option, confirm, echo, Path as ClickPath
from discord import Intents

from core.cog import default_cog_folders, load_cog_folders
from core.prefix import get_prefix
from core.set_up import set_up_bot, get_loading_message, get_bot_config
from utils.json_file import dump_file

@group()
def main():
	pass

@main.command()
@option("-C", "--config-path", type=ClickPath(exists=True, dir_okay=False, resolve_path=True), default=None, help="Path of config file")
def run(config_path):
	lrb = set_up_bot(get_prefix, intent=Intents.all())
	load_cog_folders(lrb, default_cog_folders, loading_messages=get_loading_message())
	
	# import keep_alive if bot is stable
	if lrb.stable:
		from keep_alive import keep_alive
		keep_alive()
	
	bot_token = get_bot_config("token", config_path=config_path)
	print("Starting bot")
	lrb.run(bot_token)

@main.command()
@option("--stable", type=bool, is_flag=True, help="True if this bot is stable", default=False)
@option("--owner-id", type=int, help="Bot owners ID")
def generate_bot_config(stable, owner_id):
	stable_token = prompt("Token to run stable bot(won't show anything)", default="", show_default=False, hide_input=True, type=str)
	indev_token = prompt("Token to run indev bot(won't show anything)", default="", show_default=False, hide_input=True, type=str)
	config_path = Path("bot-config.json")
	config_exist = config_path.exists()
	
	def write_config(*, overwrite=False):
		config_data = {
			"stable": stable,
			"owner": owner_id,
			"token": {
				"stable": stable_token,
				"indev": indev_token
			}
		}
		dump_file(config_data, config_path, overwrite=overwrite)
	
	if not stable_token and not indev_token:
		return echo("Aborted! Must input one of stable or indev token!")
	
	if config_exist and (overwrite := confirm("Found existing config file, overwrite it?")):
		write_config(overwrite=True)
	elif config_exist and not overwrite:
		echo("Aborted! Cancel generate config file!")
	else:
		echo("Write file to 'bot-config.json'...")
		write_config()
		echo("Done")

if len(argv) == 1:
	run()
else:
	main()
