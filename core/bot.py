from typing import TYPE_CHECKING

from disnake.ext.commands import Bot

from utils.cog import CogLoader

if TYPE_CHECKING:
    from core.config import Config


class LuxRay(Bot):
    def __init__(self, config: "Config", **options):
        super().__init__(
            command_prefix=config.prefix,
            intents=config.get_intents(),
            owner_ids=config.owner_ids,
            test_guilds=config.test_guilds if config.dev_mode else None,
            **options,
        )

        self.config = config
        self.db = config.get_database_client()

    def load_cogs(self, cog_files: list[str] = None, cog_folders: list[str] = None):
        CogLoader(self).load(files=cog_files, folders=cog_folders)
