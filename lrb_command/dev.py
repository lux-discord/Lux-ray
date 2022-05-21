from typing import TYPE_CHECKING

from disnake import ApplicationCommandInteraction
from disnake.ext.commands import Param, is_owner, slash_command

from core.cog import GeneralCog
from utils.auto_completer import cog_file_autocom, cog_folder_autocom

if TYPE_CHECKING:
    from core.bot import LuxRay


class Dev(GeneralCog):
    def cog_unload(self) -> None:
        print(f"`{self.qualified_name}` cog must be loaded, auto reload")
        self.bot.load_extension(self.qualified_name)

    @slash_command()
    @is_owner()
    async def cog(self, inter):
        pass

    @cog.sub_command()
    async def load(
        self,
        inter: ApplicationCommandInteraction,
        file: str = Param(autocomplete=cog_file_autocom, default=None),
        folder: str = Param(autocomplete=cog_folder_autocom, default=None),
    ):
        message = "Successfully loaded"

        if not (file or folder):
            self.bot.load_cogs(self.bot.cogs, self.bot.config.cog_folders)
            return await inter.send(message + " all cog files and folders")

        if file:
            message += f" cog file `{file}`"
        if folder:
            message += f" cog folder `{folder}`"

        self.bot.load_cogs([file] if file else None, [folder] if folder else None)
        await inter.send(message)

    @cog.sub_command()
    async def unload(
        self,
        inter: ApplicationCommandInteraction,
        file: str = Param(autocomplete=cog_file_autocom, default=None),
        folder: str = Param(autocomplete=cog_folder_autocom, default=None),
    ):
        message = "Successfully unloaded"

        if not (file or folder):
            self.bot.unload_cogs(self.bot.cogs, self.bot.config.cog_folders)
            return await inter.send(message + " all cog files and folders")

        if file:
            message += f" cog file `{file}`"
        if folder:
            message += f" cog folder `{folder}`"

        self.bot.unload_cogs([file] if file else None, [folder] if folder else None)
        await inter.send(message)

    @cog.sub_command()
    async def reload(
        self,
        inter: ApplicationCommandInteraction,
        file: str = Param(autocomplete=cog_file_autocom, default=None),
        folder: str = Param(autocomplete=cog_folder_autocom, default=None),
    ):
        message = "Successfully reloaded"

        if not (file or folder):
            self.bot.reload_cogs(self.bot.cogs, self.bot.config.cog_folders)
            return await inter.send(message + " all cog files and folders")

        if file:
            message += f" cog file `{file}`"
        if folder:
            message += f" cog folder `{folder}`"

        self.bot.reload_cogs([file] if file else None, [folder] if folder else None)
        await inter.send(message)

    async def test(self, inter: ApplicationCommandInteraction):
        await inter.send(type(inter.bot))


def setup(bot: "LuxRay"):
    bot.add_cog(Dev(bot))
