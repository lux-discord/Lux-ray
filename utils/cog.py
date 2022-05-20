from disnake.ext.commands import Bot
from disnake.utils import search_directory


class CogManager:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.indent = "    "
        self.file = f"file:"
        self.folder = f"folder:"

    def load_file(self, name: str):
        print(f"Load {self.file} {name}")
        self.bot.load_extension(name)

    def load_folder(self, path: str):
        print(f"Load {self.folder} {path}")
        self.bot.load_extensions(path)

    def unload_file(self, name: str):
        print(f"Unload {self.file} {name}")
        self.bot.unload_extension(name)

    def unload_folder(self, path: str):
        print(f"Unload {self.folder} {path}")
        [self.bot.unload_extension(cog) for cog in search_directory(path)]

    def reload_file(self, name: str):
        print(f"Reload {self.file} {name}")
        self.bot.reload_extension(name)

    def reload_folder(self, path: str):
        print(f"Reload {self.folder} {path}")
        [self.bot.reload_extension(cog) for cog in search_directory(path)]

    def load(self, *, files: str = None, folders: str = None):
        print("Loading cog files and folders...")

        if files:
            [self.load_file(file) for file in files]

        if folders:
            [self.load_folder(folder) for folder in folders]

    def unload(self, *, files: str = None, folders: str = None):
        print("Unloading cog files and folders...")

        if files:
            [self.unload_file(file) for file in files]

        if folders:
            [self.unload_folder(folder) for folder in folders]

    def reload(self, *, files: str = None, folders: str = None):
        print("Reloading cog files and folders...")

        if files:
            [self.reload_file(file) for file in files]

        if folders:
            [self.reload_folder(file) for file in files]
