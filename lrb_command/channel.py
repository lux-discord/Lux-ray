from typing import TYPE_CHECKING

from disnake import ApplicationCommandInteraction
from disnake.ext.commands import slash_command

from core.cog import GeneralCog
from utils.auto_completer import choose_mapping_generater

if TYPE_CHECKING:
    from core.bot import LuxRay


class Channel(GeneralCog):
    @slash_command(dm_permission=False)
    async def request(self, inter: ApplicationCommandInteraction):
        pass

    @request.sub_command()
    async def category(self, inter: ApplicationCommandInteraction, name: str):
        server = await self.get_server(inter.guild_id)

        if category_request_ch := self.bot.get_channel(server.channel.category_request):
            return await category_request_ch.send(
                f"New request! {inter.author.mention} request a category with name `{name}`"
            )

        await inter.send(
            "This server has not yet set up a channel to process category requests.\n"
            "Use `/config-channel process category-request` to set one",
            ephemeral=True,
        )

    @request.sub_command()
    async def channel(
        self, inter: ApplicationCommandInteraction, category: str, name: str
    ):
        server = await self.get_server(inter.guild_id)

        if category not in server.channel.requestable_category:
            return await server.send_ephemeral(
                inter,
                "Category `{category_name}` is not requestable",
                message_format={
                    "category_name": self.bot.get_channel(
                        int(category) if category.isalnum() else category
                    ).name
                },
            )

        if channel_request_ch := self.bot.get_channel(
            server.channel.channel_request_process_channel
        ):
            # TODO Add button
            await channel_request_ch.send(
                f"New request! {inter.author.mention} request a channel with name `{name}`"
            )

        await inter.send(
            "This server has not yet set up a channel to process channel requests.\n"
            "Use `/config-channel process channel-request` to set one",
            ephemeral=True,
        )

    @channel.autocomplete("category")
    async def channel_autocom(
        self, inter: ApplicationCommandInteraction, user_input: str = None
    ):
        server = await self.get_server(inter.guild_id)
        requestable_category = server.channel.requestable_category

        if not requestable_category:
            return ["This server has no category that allow request channels"]

        requestable_category_name_to_id = dict(
            zip(requestable_category.values(), requestable_category.keys())
        )
        return choose_mapping_generater(requestable_category_name_to_id, user_input)


"""
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
"""


def setup(bot: "LuxRay"):
    bot.add_cog(Channel(bot))
