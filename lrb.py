from sys import argv
from pathlib import Path

from click import group, option, Path as ClickPath

from core.cog import load_cogs
from core.db import MongoDB
from core.setup import setup_bot, get_bot_token, get_bot_config

@group()
def main():
	pass

@main.command()
@option("-C", "--config-path", type=ClickPath(exists=True, dir_okay=False, resolve_path=True), default="bot-config.json", help="Path of config file")
@option("-T", "--token-path", type=ClickPath(exists=True, dir_okay=False, resolve_path=True), default="bot-token.json", help="Path of token file")
@option("-M", "--mode", default="dev", help="Which mode should bot run on")
def run(config_path, token_path, mode):
	# Prepare
	config = get_bot_config(config_path, mode)
	token = get_bot_token(token_path, mode)
	lrb = setup_bot(config, mode, MongoDB(db_host=config["db_host"], db_port=config["db_port"]))
	
	# Load cogs
	load_cogs(bot, cogs=config["cog_path"], cog_folders=config["cog_folder_path"])
	
	# Run
	lrb.run(token)

if len(argv) == 1:
	run()
else:
	main()
