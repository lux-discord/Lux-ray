from sys import argv
from pathlib import Path

from click import group, option, Path as ClickPath

from core.setup import setup_bot, get_bot_token

@group()
def main():
	pass

@main.command()
@option("-C", "--config-path", type=ClickPath(exists=True, dir_okay=False, resolve_path=True), default=None, help="Path of config file")
@option("-T", "--token-path", type=ClickPath(exists=True, dir_okay=False, resolve_path=True), default=None, help="Path of token file")
def run(config_path, token_path):
	lrb = setup_bot(config_path)
	
	# import keep_alive if bot is in stable mode
	if lrb.mode == "stable":
		from keep_alive import keep_alive
		keep_alive()
	
	bot_token = get_bot_token(token_path, mode=lrb.mode)
	lrb.run(bot_token)

if len(argv) == 1:
	run()
else:
	main()
