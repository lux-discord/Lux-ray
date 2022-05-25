from typing import TYPE_CHECKING

from disnake import ApplicationCommandInteraction, CategoryChannel, PermissionOverwrite
from disnake.ext.commands import slash_command

from core.cog import GeneralCog

if TYPE_CHECKING:
    from core.bot import LuxRay


class Channel(GeneralCog):
    @slash_command(dm_permission=False)
    async def request(self, inter: ApplicationCommandInteraction):
        pass

    @request.sub_command()
    async def category(self, inter: ApplicationCommandInteraction, name: str):
        pass

    @request.sub_command()
    async def channel(
        self, inter: ApplicationCommandInteraction, category: CategoryChannel, name: str
    ):
        server = await self.get_server(inter.guild_id)
        rable_category_id_to_name = {
            rable_category.id: rable_category.name
            for cid in server.channel.requestable_category
            if (rable_category := self.bot.get_channel(cid))
        }

        if category.id not in rable_category_id_to_name:
            return await inter.send(
                f"Requestable categories: `{', '.join(rable_category_id_to_name.values())}`",
                ephemeral=True,
            )

        overwrites = {
            inter.author: PermissionOverwrite(manage_channels=True, send_messages=True)
        }

        if (gdefault_role := inter.guild.default_role) in category.overwrites:
            gdefault_role_overwrite = category.overwrites_for(gdefault_role)
            gdefault_role_overwrite.send_messages = False
            overwrites[gdefault_role] = gdefault_role_overwrite

        channel = await category.create_text_channel(name)
        await channel.edit(overwrites=overwrites)
        await inter.send(
            f"Channel {channel.mention} created in category `{category.name}`",
            ephemeral=True,
        )


def setup(bot: "LuxRay"):
    bot.add_cog(Channel(bot))
