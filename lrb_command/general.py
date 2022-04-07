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
		embed_text = {
			"Emoji info": server.translate("Emoji info"),
			"Name": server.translate("Name"),
			"Created at": server.translate("Created at"),
			"Url": server.translate("Url")
		}
		base_emoji_url = "https://cdn.discordapp.com/emojis/"
		
		def generate_embed(emoji: Emoji):
			embed = Embed(title=embed_text["Emoji info"], color=bot_color)
			fields = [
				[embed_text["Name"], f"`{emoji.name}`"],
				[embed_text["Created at"], emoji.created_at.strftime("%Y-%m-%d %H:%M:%S")],
				[embed_text["Url"], emoji.url, False]
			]
			
			return embed_setup(embed, fields=fields)
		
		def generate_embed_with_id(emoji_id: int):
			embed = Embed(title=embed_text["Emoji info"], color=bot_color)
			fields = [
				[embed_text["Url"], base_emoji_url+str(emoji_id), False]
			]
			return embed_setup(embed, fields=fields)
		
		if emojis:
			return [await ctx.send(embed=generate_embed(emoji)) for emoji in emojis]
		
		async with target_message(ctx) as message:
			match_emojis = findall(r"<a?:[a-zA-Z0-9\_]{1,32}:([0-9]{15,20})>$", message.content)
			return [await ctx.send(
				embed=generate_embed(emoji) if (emoji := self.bot.get_emoji(int(emoji_id))) else generate_embed_with_id(int(emoji_id))
				) for emoji_id in match_emojis]

def setup(bot):
	bot.add_cog(General(bot))
