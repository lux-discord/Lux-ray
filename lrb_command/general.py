from re import findall

from disnake.embeds import Embed
from disnake.emoji import Emoji
from disnake.ext.commands import command

from core.cog import GeneralCog
from utils.embed import bot_color, embed_setup
from utils.message import target_message


class General(GeneralCog):
	@command(aliases=["emoji"])
	async def emoji_info(self, ctx, *emojis: Emoji):
		server = await self.get_server(ctx.guild.id)
		embed_fields_name = {
			"Name": server.translate("Name"),
			"Created at": server.translate("Created at"),
			"Url": server.translate("Url")
		}
		
		def generate_embed(emoji: Emoji):
			embed = Embed(title=server.translate("Emoji info"), color=bot_color)
			fields = [
				[embed_fields_name["Name"], f"`{emoji.name}`"],
				[embed_fields_name["Created at"], emoji.created_at.strftime("%Y-%m-%d %H:%M:%S")],
				[embed_fields_name["Url"], emoji.url, False]
			]
			
			return embed_setup(embed, fields=fields)
		
		if emojis:
			return [await ctx.send(embed=generate_embed(emoji)) for emoji in emojis]
		
		async with target_message(ctx) as message:
			match_emojis = findall(r"<a?:[a-zA-Z0-9\_]{1,32}:([0-9]{15,20})>$", message.content)
			return [await ctx.send(embed=generate_embed(emoji)) for emoji in match_emojis]

def setup(bot):
	bot.add_cog(General(bot))
