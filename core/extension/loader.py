from exceptions import InvalidExtension
from pathlib import Path

from .manifest import Manifest

def extension_cog_loader(bot, extension_path: Path):
	try:
		manifest = Manifest(extension_path)
	except FileNotFoundError:
		# Manifest file not exist
		raise InvalidExtension(str(extension_path))
	
	for cog in manifest.generate_cog():
		print(f"        {cog.split('.')[-1]}")
		bot.load_extension(cog)
