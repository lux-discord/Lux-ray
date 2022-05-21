from datetime import date
from re import findall
from typing import TYPE_CHECKING

from disnake import ApplicationCommandInteraction, Embed, Emoji
from disnake.ext.commands import slash_command

from core.cog import GeneralCog
from utils.embed import BOT_COLOR
from utils.message import TargetMessageInter

if TYPE_CHECKING:
    from core.bot import LuxRay


class General(GeneralCog):
    @slash_command()
    async def emoji_info(
        self, inter: ApplicationCommandInteraction, emoji: Emoji = None
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

        def generate_emoji_embed(emoji: Emoji):
            return (
                base_embed.add_field(embed_text["Name"], f"`{emoji.name}`")
                .add_field(
                    embed_text["Created at"],
                    f"`{emoji.created_at.strftime('%Y-%m-%d %H:%M:%S')}`",
                )
                .add_field(embed_text["Url"], emoji.url, inline=False)
            )

        if emoji:
            return await inter.send(
                embed=generate_emoji_embed(emoji),
                ephemeral=True,
            )

        async with TargetMessageInter(inter) as message:
            match_emojis = findall(
                r"<a?:[a-zA-Z0-9\_]{1,32}:([0-9]{15,20})>$", message.content
            )

            [
                await inter.send(
                    embed=generate_emoji_embed(emoji),
                    ephemeral=True,
                )
                if (emoji := self.bot.get_emoji(int(emoji_id)))
                else await inter.send(
                    embed=base_embed.add_field(
                        embed_text["Url"], base_emoji_url + emoji_id, inline=False
                    ),
                    ephemeral=True,
                )
                for emoji_id in match_emojis
            ] if match_emojis else await inter.send(
                "There is not emoji in the last message of this channel",
                ephemeral=True,
            )

    @slash_command()
    async def login(self, inter: ApplicationCommandInteraction):
        user = await self.get_user(inter.author.id)
        today = str(date.today())

        if user.last_login == today:
            return await inter.send(
                f"You are already logged in today. Days: {user.login_days}",
                ephemeral=True,
            )

        login_days = user.login_days + 1
        await self.update_user(user.UserData(login_days=login_days, last_login=today))
        await inter.send(
            f"Login success, you already login {login_days} days", ephemeral=True
        )


def setup(bot: "LuxRay"):
    bot.add_cog(General(bot))
