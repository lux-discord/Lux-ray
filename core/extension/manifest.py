from pathlib import Path
from typing import Union

from exceptions import InvalidExtension
from tool import load_file


class Manifest():
	def __init__(self, extension_path: Path) -> None:
		# findout menifest file
		for file in extension_path.iterdir():
			if file.is_file() and file.stem in {"manifest", "MANIFEST", "Manifest"}:
				self.data = load_file(file)
		
		# if manifest file not exist, raise InvalidExtension
		if not hasattr(self, "data"):
			raise InvalidExtension(extension_path)
		
		self.extension_path = extension_path
		self.name: str = self.data.get("name", str(extension_path))
		self.description: Union[str, None] = self.data.get("description", self.data.get("desc", None))
		self.commands: Union[list[str], None] = self.data.get("commands", None)
	
	def generate_cog(self):
		for command in self.commands:
			yield str(self.extension_path/command.removesuffix(".py")).replace("\\", ".")
