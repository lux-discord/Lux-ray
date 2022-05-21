from typing import TYPE_CHECKING

from disnake.ext.commands import Bot
from disnake.utils import search_directory

if TYPE_CHECKING:
    from typing import Iterable


class CogManager:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.indent = "    "
        self.file = "file:"
        self.folder = "folder:"

    def load_file(self, name: str):
        print(f"{self.indent}Load {self.file} {name}")
        self.bot.load_extension(name)

    def load_folder(self, path: str):
        print(f"{self.indent}Load {self.folder} {path}")
        self.bot.load_extensions(path)

    def unload_file(self, name: str):
        print(f"{self.indent}Unload {self.file} {name}")
        self.bot.unload_extension(name)

    def unload_folder(self, path: str):
        print(f"{self.indent}Unload {self.folder} {path}")
        [self.bot.unload_extension(cog) for cog in search_directory(path)]

    def reload_file(self, name: str):
        print(f"{self.indent}Reload {self.file} {name}")
        self.bot.reload_extension(name)

    def reload_folder(self, path: str):
        print(f"{self.indent}Reload {self.folder} {path}")
        [self.bot.reload_extension(cog) for cog in search_directory(path)]

    def load(self, *, files: "Iterable[str]" = None, folders: "Iterable[str]" = None):
        print("Loading cog files and folders...")

        if files:
            [self.load_file(file) for file in files]
        if folders:
            [self.load_folder(folder) for folder in folders]

    def unload(self, *, files: "Iterable[str]" = None, folders: "Iterable[str]" = None):
        print("Unloading cog files and folders...")

        if files:
            [self.unload_file(file) for file in files]

        if folders:
            [self.unload_folder(folder) for folder in folders]

    def reload(self, *, files: "Iterable[str]" = None, folders: "Iterable[str]" = None):
        print("Reloading cog files and folders...")

        if files:
            [self.reload_file(file) for file in files]

        if folders:
            [self.reload_folder(file) for file in files]
