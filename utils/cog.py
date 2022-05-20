from disnake.ext.commands import Bot
from disnake.utils import search_directory


class CogManager:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.indent = "    "
        self.file_message = f"{self.indent}File: "
        self.folder_message = f"{self.indent}Folder: "

    def load_file(self, name: str):
        print(self.file_message + name)
        self.bot.load_extension(name)

    def load_folder(self, path: str):
        print(self.folder_message + path)
        self.bot.load_extensions(path)

    def unload_file(self, name: str):
        print(self.file_message + name)
        self.bot.unload_extension(name)

    def unload_folder(self, path: str):
        print(self.folder_message + path)
        [self.bot.unload_extension(cog) for cog in search_directory(path)]

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
            [self.unload_file(file) for file in files]
            [self.load_file(file) for file in files]

        if folders:
            [self.unload_folder(folder) for folder in folders]
            [self.load_folder(folder) for folder in folders]
