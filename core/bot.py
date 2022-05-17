from typing import TYPE_CHECKING

from disnake.ext.commands import Bot

from utils.cog import CogLoader

if TYPE_CHECKING:
    from core.config import Config


class LuxRay(Bot):
    def __init__(self, config: "Config", **options):
        self.config = config
        self.db = config.get_database_client()
        self.mode = config.mode
        self.dev_mode = self.mode == "DEV"

        super().__init__(
            command_prefix=self.config.prefix,
            intents=self.config.get_intents(),
            owner_ids=self.config.owner_ids,
            test_guilds=self.config.test_guilds if self.dev_mode else None,
            **options,
        )

    def load_cogs(self, cog_files: list[str] = None, cog_folders: list[str] = None):
        CogLoader(self).load(files=cog_files, folders=cog_folders)
