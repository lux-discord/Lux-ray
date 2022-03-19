from sys import argv

from click import group, option, Path as ClickPath

from core.setup import setup_bot, get_bot_config
from core.config import get_bot_token
from utils.cog import load_cogs

@group()
def main():
	pass

@main.command()
@option("-M", "--mode", default="dev", show_default=True, help="Which mode should bot run on")
@option("-C", "--config-path", default="bot-config.toml", show_default=True, type=ClickPath(exists=True, dir_okay=False, resolve_path=True), help="Path of config file")
def run(mode="dev", config_path="bot-config.toml"):
	# Prepare
	config = get_bot_config(config_path)
	token = get_bot_token(config, mode)
	bot = setup_bot(config, mode)
	
	# Load cogs
	load_cogs(bot, cogs=config["cogs"]["file"], cog_folders=config["cogs"]["folder"])
	
	# Run
	bot.run(token)

if len(argv) == 1:
	run()
else:
	main()
