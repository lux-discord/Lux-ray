from re import findall
from typing import TYPE_CHECKING

from disnake import ApplicationCommandInteraction, Embed, Emoji
from disnake.ext.commands import slash_command

from core.cog import GeneralCog
from utils.embed import BOT_COLOR
from utils.message import TargetMessage

if TYPE_CHECKING:
    from core.bot import LuxRay


class General(GeneralCog):
    @slash_command()
    async def tools(self, inter: ApplicationCommandInteraction):
        pass

    @tools.sub_command(name="emoji-info")
    async def emoji_info(
        self,
        inter: ApplicationCommandInteraction,
        emoji: Emoji = None,
        message_link: str = "",
    ):
        server = await self.get_server(inter.guild_id)
        embed_text = {
            "Emoji info": server.translate("Emoji info"),
            "Name": server.translate("Name"),
            "Created at": server.translate("Created at"),
            "Url": server.translate("Url"),
        }
        base_embed = Embed(title=embed_text["Emoji info"], color=BOT_COLOR)
        base_emoji_url = "https://cdn.discordapp.com/emojis/"
        emoji_pattern = r"<a?:[a-zA-Z0-9\_]{1,32}:([0-9]{15,20})>$"

        def emoji_info_embed(emoji_id: int):
            if emoji := self.bot.get_emoji(emoji_id):
                emoji_create_time = emoji.created_at.strftime("%Y-%m-%d %H:%M:%S")

                return (
                    base_embed.add_field(embed_text["Name"], f"`{emoji.name}`")
                    .add_field(embed_text["Created at"], f"`{emoji_create_time}`")
                    .add_field(embed_text["Url"], emoji.url, inline=False)
                )
            return base_embed.add_field(
                embed_text["Url"], base_emoji_url + emoji_id, inline=False
            )

        if emoji:
            return await inter.send(
                embed=emoji_info_embed(emoji.id),
                ephemeral=True,
            )

        async with TargetMessage(
            inter, message_link=message_link, last_message=True
        ) as message:
            if match_emoji_ids := findall(emoji_pattern, message.content):
                return [
                    await inter.send(
                        embed=emoji_info_embed(int(emoji_id)), ephemeral=True
                    )
                    for emoji_id in match_emoji_ids
                ]

            await inter.send(
                "There is no emoji in the last message of this channel",
                ephemeral=True,
            )


def setup(bot: "LuxRay"):
    bot.add_cog(General(bot))
