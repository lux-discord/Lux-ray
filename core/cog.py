from pathlib import Path

from disnake.ext.commands import Bot


class BaseLoader():
	def __init__(self, bot: Bot) -> None:
		self.bot = bot
	
	def file_loader():
		raise NotImplementedError
	
	def folder_loader():
		raise NotImplementedError
	
	def load(self, *, files=None, folders=None):
		if files:
			for file in files:
				self.file_loader(Path(file))
		
		if folders:
			for folder in folders:
				self.folder_loader(Path(folder))

class CogLoader(BaseLoader):
	def file_loader(self, cog: Path):
		print(f"	{cog}")
		self.bot.load_extension(cog)
	
	def folder_loader(self, folder: Path, indent_lv=None):
		indent_lv = 1 if not indent_lv else indent_lv
		print(f"{'	'*indent_lv}{folder.name}")
		
		for item in folder.iterdir():
			if item.is_file() and item.suffix == ".py" and not item.name.startswith("_"):
				print(f"{'	'*indent_lv+1}{item.stem}")
				# replace "/" with "." and remove suffix
				cog_path = ".".join(item.with_name(item.stem).parts)
				self.bot.load_extension(cog_path)
			elif item.is_dir():
				self.folder_loader(bot, item, indent_lv=indent_lv+1)

def load_cogs(bot, *, cogs=None, cog_folders=None):
	CogLoader(bot).load(files=cogs, folders=cog_folders)
