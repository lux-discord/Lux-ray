from discord.errors import HTTPException
from core import InitedCog, Server
from discord.ext.commands.core import command, has_permissions
from exceptions import InvalidMessageLink
from tool.message import send_error, send_info


def message_link_parser(message_link: str):
	link_prefix = "https://discord.com/channels/"
	
	if link_prefix in message_link:
		try:
			return message_link.removeprefix("https://discord.com/channels/").split("/")[1:]
		except IndexError:
			raise InvalidMessageLink(message_link)

@has_permissions(manage_messages = True)
class Messages(InitedCog):
	@command()
	async def pin(self, ctx, message_link: str=None):
		ctx_message = ctx.message
		ctx_channel = ctx.channel
		server = Server(ctx)
		
		async def pin_message(message, channel):
			await message.pin(reason=server.lang_request("audit_log.reason.message.pin_message"))
			
			async for message in channel.history(limit=7):
				if not message.content:
					await message.delete()
					break
		
		await ctx_message.delete()
		
		if message_link:
			try:
				channel_id, message_id = message_link_parser(message_link) # may raise InvalidMessageLink
				
				# channel exist
				if channel := self.bot.get_channel(int(channel_id)):
					# have permission in target channel
					if channel.permissions_for(ctx.author).manage_messages:
						# message exist
						try:
							message = await channel.fetch_message(int(message_id))
						except HTTPException:
							raise InvalidMessageLink(message_link)
					else:
						raise InvalidMessageLink(message_link)
				else:
					raise InvalidMessageLink(message_link)
				
				# message not pinned
				if not message.pinned:
					await pin_message(message, channel)
				
				await send_info(ctx, server.lang_request("info.message.pinned_message"))
			except InvalidMessageLink as error:
				return await send_error(ctx, server.lang_request("error.invalid_argument.invalid_message_link").format(message_link=error.args[0]))
		elif refer_mes := ctx_message.reference:
			refer_mes = refer_mes.resolved
			
			if not refer_mes.pinned:
				await pin_message(refer_mes, ctx_channel)
			
			await send_info(ctx, server.lang_request("info.message.pinned_message"))
		else:
			async for message in ctx_channel.history(limit=1):
				if not message.pinned:
					await pin_message(message, ctx_channel)
			
			await send_info(ctx, server.lang_request("info.message.pinned_message"))
	
	@command()
	async def unpin(self, ctx, message_url: str=None):
		pass
	
	@command(aliases = ["del_mes", "del_msg", "purge"])
	async def delete_message(self, ctx, delete_num=1):
		await ctx.channel.purge(limit=delete_num + 1)
		await send_info(ctx, Server(ctx).lang_request("info.message.deleted_message").format(deleted_number=delete_num))


def setup(bot):
	bot.add_cog(Messages(bot))
