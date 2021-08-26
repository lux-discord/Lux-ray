from re import compile

from core import InitedCog, Server
from discord.embeds import Embed
from discord.ext.commands.core import command
from exceptions import InvalidEmojiError
from tool.embed import bot_color, embed_setup
from tool.message import send_error

emoji_regex = compile(r"<a?:(.+?:[0-9]{15,21})>")

class Common(InitedCog):
	@command(aliases=["emoji"])
	async def emoji_info(self, ctx, *emojis):
		server = Server(ctx)
		
		def parse_raw_emojis(*raw_emojis: str) -> set[tuple[str, str]]:
			"""
			Parse `raw_emoji` to (`emoji_name`, `emoji_id`)
			
			Raise
			-----
			`InvalidEmojiError`: If the text in raw_emojis is not a valid emoji format
			
			Return format
			------
			{ (`emoji_name`, `emoji_id`)* }
			"""
			def parser(raw_emoji):
				try:
					return emoji_regex.findall(raw_emoji)[0].split(":")
				except IndexError:
					# IndexError -> no valid emoji text found
					raise InvalidEmojiError(raw_emoji)
			# Use the `parser` function to point out the wrong text
			# return set type to remove duplicate emoji
			return {tuple(parser(raw_emoji)) for raw_emoji in raw_emojis}
			
		def generate_embed(emoji: tuple[str, str]):
			embed = Embed(title="Emoji info", color=bot_color)
			emoji_name, emoji_id = emoji
			
			if emoji := self.bot.get_emoji(int(emoji_id)):
				fields = [
					["Name", f"`{emoji.name}`"],
					["Created at", emoji.created_at.strftime("%Y-%m-%d %H:%M:%S")],
					["Url", emoji.url, False]
				]
				return embed_setup(embed, fields=fields, image_url=emoji.url)
			
			emoji_url = "https://cdn.discordapp.com/emojis/" + emoji_id
			fields = [
				["Name", emoji_name],
				["Url", emoji_url, False]
			]
			return embed_setup(embed, fields=fields, image_url=emoji_url)
		
		if emojis:
			# `emojis` may invalid
			try:
				emojis = parse_raw_emojis(*emojis)
			except InvalidEmojiError as error:
				return await send_error(ctx,
					server.lang_request("error.invalid_argument.invalid_emoji").format(invalid_emoji_text=error.args[0]))
			return [await ctx.send(embed=generate_embed(emoji)) for emoji in emojis]
		if refer_mes := ctx.message.reference:
			if emojis := emoji_regex.findall(refer_mes.resolved.content):
				emojis: set[list[str, str]] = {tuple(emoji.split(":")) for emoji in emojis}
				return [await ctx.send(embed=generate_embed(emoji)) for emoji in emojis]
			return await send_error(ctx, server.lang_request("error.target_not_found.reference_message_has_no_emoji"))
		await send_error(ctx, server.lang_request("error.target_not_found.no_emoji_input"))
	
	@command(aliases=["mes_link", "msg_link"])
	async def message_link(self, ctx):
		if refer_mes := ctx.message.reference:
			return await ctx.send(refer_mes.jump_url)
		await ctx.send(Server(ctx).lang_request("error.target_not_found.no_reference_message"))

def setup(bot):
	bot.add_cog(Common(bot))
