from re import findall
from typing import TYPE_CHECKING

from disnake import ApplicationCommandInteraction, Embed, Emoji
from disnake.ext.commands import message_command, slash_command
from disnake.ext.commands.errors import EmojiNotFound
from pysaucenao import SauceNao

from core.cog import GeneralCog
from utils.embed import BOT_COLOR
from utils.message import TargetMessage

if TYPE_CHECKING:
    from pysaucenao.containers import SauceNaoResults

    from core.bot import LuxRay
    from core.server import Server


class General(GeneralCog):
    # Internal logic
    def __RIS_results_info_embed(self, server: "Server", results: "SauceNaoResults"):
        embed_text = {
            "Author": server.translate("Author"),
            "Title": server.translate("Title"),
            "Similarity": server.translate("Similarity"),
        }
        base_embed = Embed(color=BOT_COLOR)

        for result in results:
            base_embed.add_field(
                embed_text["Author"], result.author_name, inline=False
            ).add_field(embed_text["Title"], result.title).add_field(
                embed_text["Similarity"], result.similarity
            ).add_field(
                "Url", result.url, inline=False
            )

        return base_embed.set_image(results[0].url)

    # Commands
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
                embed_text["Url"], base_emoji_url + str(emoji_id), inline=False
            )

        if emoji:
            return await server.send_ephemeral(inter, embed=emoji_info_embed(emoji.id))

        async with TargetMessage(
            inter, message_link=message_link, last_message=True
        ) as message:
            if match_emoji_ids := findall(emoji_pattern, message.content):
                return [
                    await server.send_ephemeral(
                        inter, embed=emoji_info_embed(int(emoji_id))
                    )
                    for emoji_id in match_emoji_ids
                ]

            await server.send_ephemeral(
                inter, "There is no emoji in the last message of this channel"
            )

    @tools.sub_command(name="reverse-image-search")
    async def reverse_image_search(
        self,
        inter: ApplicationCommandInteraction,
        image_url: str,
    ):
        await inter.response.defer(with_message=True, ephemeral=True)
        server = await self.get_server(inter.guild_id)
        sauce = SauceNao(api_key=self.bot.config.saucenao_api_key)

        results = await sauce.from_url(image_url)
        await server.send_ephemeral(
            inter, embed=self.__RIS_results_info_embed(server, results)
        )
        return await server.send_ephemeral(
            inter,
            "Searches remaining today: {times}",
            message_format={"times": results.long_remaining},
        )

    # Message command
    @message_command(name="reverse image search")
    async def message_reverse_image_search(self, inter: ApplicationCommandInteraction):
        await inter.response.defer(with_message=True, ephemeral=True)
        server = await self.get_server(inter.guild_id)
        sauce = SauceNao(api_key=self.bot.config.saucenao_api_key)

        if attachments := inter.target.attachments:
            results = await sauce.from_url(attachments[0].url)
            await server.send_ephemeral(
                inter, embed=self.__RIS_results_info_embed(server, results)
            )
            return await server.send_ephemeral(
                inter,
                "Searches remaining today: {times}",
                message_format={"times": results.long_remaining},
            )

        await server.send_ephemeral(inter, "There are no pictures in this message")

    # Local error handler
    @emoji_info.error
    async def emoji_info_error(self, inter: ApplicationCommandInteraction, error):
        if isinstance(error, EmojiNotFound):
            server = await self.get_server(inter.guild_id)
            await server.send_ephemeral(
                inter,
                "`{emoji}` is not a valid emoji",
                message_format={"emoji": error.argument},
            )


def setup(bot: "LuxRay"):
    bot.add_cog(General(bot))
