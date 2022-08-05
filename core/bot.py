from typing import TYPE_CHECKING

from disnake.ext.commands import InteractionBot

from core.config import Config
from utils.cog import CogManager

if TYPE_CHECKING:
    from pathlib import Path


class LuxRay(InteractionBot):
    def __init__(self, config_path: "Path", mode: str, **options):
        config = Config(config_path, mode)
        super().__init__(
            intents=config.intents,
            owner_ids=options.get("owner_ids", config.owner_ids),
            test_guilds=options.get("test_guilds", config.test_guilds)
            if config.is_dev
            else None,
            **options,
        )

        self.config = config
        self.mode = mode
        self.is_dev = config.is_dev
        self.db = config.database
        self.cog_manager = CogManager(self)

    def init(self):
        self.cog_manager.load(
            files=self.config.cog_files, folders=self.config.cog_folders
        )

        if not self.is_dev:
            from keep_alive import keep_alive

            keep_alive()

    def run(self, *, reconnect: bool = True) -> None:
        return super().run(self.config.bot_token, reconnect=reconnect)

    def load_cogs(self, cog_files: list[str] = None, cog_folders: list[str] = None):
        self.cog_manager.load(files=cog_files, folders=cog_folders)

    def unload_cogs(self, cog_files: list[str] = None, cog_folders: list[str] = None):
        self.cog_manager.unload(files=cog_files, folders=cog_folders)

    def reload_cogs(self, cog_files: list[str] = None, cog_folders: list[str] = None):
        self.cog_manager.reload(files=cog_files, folders=cog_folders)
