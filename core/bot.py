from typing import TYPE_CHECKING

from disnake.ext.commands import InteractionBot

from utils.cog import CogManager

if TYPE_CHECKING:
    from core.config import Config


class LuxRay(InteractionBot):
    def __init__(self, config: "Config", **options):
        super().__init__(
            command_prefix=config.prefix,
            intents=config.create_intents(),
            owner_ids=config.owner_ids,
            test_guilds=config.test_guilds if config.dev_mode else None,
            **options,
        )

        self.config = config
        self.db = config.create_database_client()
        self.cog_manager = CogManager(self)

    def load_cogs(self, cog_files: list[str] = None, cog_folders: list[str] = None):
        self.cog_manager.load(files=cog_files, folders=cog_folders)

    def unload_cogs(self, cog_files: list[str] = None, cog_folders: list[str] = None):
        self.cog_manager.unload(files=cog_files, folders=cog_folders)

    def reload_cogs(self, cog_files: list[str] = None, cog_folders: list[str] = None):
        self.cog_manager.reload(files=cog_files, folders=cog_folders)
