from re import findall

from disnake.embeds import Embed
from disnake.emoji import Emoji
from disnake.ext.commands import command

from core.cog import GeneralCog
from utils.embed import bot_color, embed_setup
from utils.message import target_message


class Common(GeneralCog):
	@command(aliases=["emoji"])
	async def emoji_info(self, ctx, *emojis: Emoji):
		def generate_embed(emoji: Emoji):
			embed = Embed(title="Emoji info", color=bot_color)
			fields = [
				["Name", f"`{emoji.name}`"],
				["Created at", emoji.created_at.strftime("%Y-%m-%d %H:%M:%S")],
				["Url", emoji.url, False]
			]
			
			return embed_setup(embed, fields=fields)
		
		if emojis:
			return [await ctx.send(embed=generate_embed(emoji)) for emoji in emojis]
		
		async with target_message(ctx) as message:
			match_emojis = findall(r"<a?:[a-zA-Z0-9\_]{1,32}:([0-9]{15,20})>$", message.content)
			return [await ctx.send(embed=generate_embed(emoji)) for emoji in match_emojis]

def setup(bot):
	bot.add_cog(Common(bot))
