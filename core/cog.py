from pathlib import Path

from disnake.ext.commands.bot import Bot

from exceptions import InvalidExtension
from core.extension.loader import extension_cog_loader

class InitedCog(Cog):
	def __init__(self, bot: Bot) -> None:
		self.bot = bot

def load_cogs(bot, *, cogs=None, cog_folders=None):
	def folder_loader(bot, folder: Path, *, indent_lv: int=None):
		indent_lv = 1 if not indent_lv else indent_lv
		print(f"{'	'*indent_lv}{folder}")
		
		for item in folder.iterdir():
			if item.is_file() and item.suffix == ".py" and not item.name.startswith("_"):
				print(f"{'	'*indent_lv+1}{item.name}")
			elif item.is_dir():
				folder_loader(bot, item, indent_lv=indent_lv+1)
	
	if cogs:
		for cog in cogs:
			print(f"	{cog}")
			bot.load_extension(cogs)
	
	if cog_folders:
		for folder in cog_folders:
			folder_loader(bot, Path(folder))
