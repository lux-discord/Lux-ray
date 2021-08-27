from pathlib import Path

from discord.ext.commands.bot import Bot
from discord.ext.commands.cog import Cog
from exceptions import InvalidExtension

from .extension.loader import extension_cog_loader

cog_folders = [
	"lrb_backend",
	"lrb_command",
	"lrb_extension"
]
cog_folder_abbr = [
	"be",
	"cmd",
	"ext"
]
cog_folder_abbr_to_fullname = dict(zip(cog_folder_abbr, cog_folders))

class InitedCog(Cog):
	def __init__(self, bot: Bot) -> None:
		self.bot = bot

def cog_folder_dict_generater(folder):
	"""Generate dict with gived folder
	
	file startwith `_` won't in the dict
	
	Return
	------
	format: {`file.stem` : `folder_path` . `file.stem`}
	"""
	folder_path = Path(folder)
	
	return {file.stem: f"{folder_path}.{file.stem}" for file in folder_path.iterdir() if file.is_file() and not str(file).startswith("_") and file.suffix == ".py"}

def cog_folder_loader(bot, folder):
	if folder == cog_folder_abbr_to_fullname["ext"]:
		for extension_folder in Path(folder).iterdir():
			print(f"    {extension_folder.name}")
			
			try:
				extension_cog_loader(bot, extension_folder)
			except InvalidExtension:
				raise InvalidExtension(extension_folder)
	else:
		cog_dict = cog_folder_dict_generater(folder)
		
		for file, cog in cog_dict.items():
			print(f"    {file}")
			bot.load_extension(cog)
