from sys import argv

from pathlib import Path
from click import Path as ClickPath, group, option
from core.config import get_bot_token
from core.setup import get_bot_config, setup_bot
from dotenv import load_dotenv
from utils.cog import load_cogs

ENV_FILE_PATH = Path(".env")

if ENV_FILE_PATH.exists():
	load_dotenv(ENV_FILE_PATH)

@group()
def main():
	pass

@main.command()
@option("-M", "--mode", default="dev", show_default=True, help="Which mode should bot run on")
@option("-C", "--config-path", default="bot-config.toml", show_default=True, type=ClickPath(exists=True, dir_okay=False, resolve_path=True), help="Path of config file")
def run(mode="dev", config_path="bot-config.toml"):
	# Prepare
	config = get_bot_config(config_path)
	token = get_bot_token(mode)
	bot = setup_bot(config, mode)
	
	# Load cogs
	load_cogs(bot, cogs=config["cogs"]["file"], cog_folders=config["cogs"]["folder"])
	
	# Run
	bot.run(token)

if len(argv) == 1:
	run()
else:
	main()
