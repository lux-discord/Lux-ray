from disnake import ApplicationCommandInteraction
from disnake.ext.commands import Cog

from core.cog import GeneralCog


class ExtEvent(GeneralCog):
    @Cog.listener()
    async def on_slash_command_error(self, inter: ApplicationCommandInteraction, error):
        if inter.application_command.has_error_handler():
            return

        raise error


def setup(bot):
    bot.add_cog(ExtEvent(bot))
