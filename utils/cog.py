from pathlib import Path
from typing import TYPE_CHECKING

from disnake.ext.commands import Bot

if TYPE_CHECKING:
    from typing import Union


class CogLoader:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.indent = "    "

    def file_loader(self, cog: Path):
        print(f"{self.indent}File: {cog}")
        self.bot.load_extension(cog)

    def folder_loader(self, folder: Path, *, indent_lv=None):
        indent_lv = indent_lv or 1
        print(f"{self.indent*indent_lv}Folder: {folder.name}")

        for item in folder.iterdir():
            if (
                item.is_file()
                and item.suffix == ".py"
                and not item.name.startswith("_")
            ):
                print(f"{self.indent*(indent_lv+1)}File: {item.stem}")
                # replace "/" with "." and remove suffix
                cog_file_path = ".".join(item.with_name(item.stem).parts)
                self.bot.load_extension(cog_file_path)
            elif item.is_dir() and not item.name.startswith("_"):
                self.folder_loader(item, indent_lv=indent_lv + 1)

    def load(
        self, *, files: "Union[str, Path]" = None, folders: "Union[str, Path]" = None
    ):
        print("Loading cog files and folders...")

        if files:
            [
                self.file_loader(file)
                if isinstance(file, Path)
                else self.file_loader(Path(file))
                for file in files
            ]

        if folders:
            [
                self.folder_loader(folder)
                if isinstance(folder, Path)
                else self.folder_loader(Path(folder))
                for folder in folders
            ]
