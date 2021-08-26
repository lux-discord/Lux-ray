from core import InitedCog, Server
from discord.channel import TextChannel
from discord.errors import HTTPException
from discord.ext.commands.core import command, has_permissions
from discord.message import Message
from exceptions import InvalidChannelID, InvalidMessageID, InvalidMessageLink
from tool.message import send_error, send_info


@has_permissions(manage_messages = True)
class Messages(InitedCog):
	async def message_link_parser(self, message_link: str):
		"""
		Parameter
		---------
		message_link: `str`
			a link that contain may "https://discord.com/channels/"
		
		Raise
		-----
		InvalidMessageLink: when `message_link` is incomplete
		InvalidChannelID: when chennel is not exist
		InvalidMessageID: when channel is not readable for bot or message doesn't exist
		"""
		link_prefix = "https://discord.com/channels/" 
		
		if link_prefix in message_link:
			try:
				channel_id, message_id = message_link.removeprefix("https://discord.com/channels/").split("/")[1:]
				
				channel: TextChannel = self.bot.get_channel(int(channel_id))
				message: Message = await channel.fetch_message(int(message_id))
				return channel, message
			except ValueError:
				# `message_link` is incomplete
				raise InvalidMessageLink(message_link)
			except AttributeError:
				# 'NoneType' object has no 'fetch_message' attribute -> channel doesn't exist
				raise InvalidChannelID(channel_id)
			except HTTPException:
				# channel not readable or message doesn't exist
				raise InvalidMessageID(message_id)
		else:
			raise InvalidMessageLink(message_link)
	
	async def process_message_link(self, message_link, process, ctx, server: Server):
		try:
			channel, message = await self.message_link_parser(message_link)
			await process(channel, message)
		except InvalidMessageLink as error:
			await send_error(ctx, server.lang_request("error.invalid_argument.invalid_message_link").format(message_link=error.args[0]))
		except InvalidChannelID as error:
			await send_error(ctx, server.lang_request("error.invalid_argument.invalid_channel_id").format(channel_id=error.args[0]))
		except InvalidMessageID as error:
			await send_error(ctx, server.lang_request("error.invalid_argument.invalid_message_id").format(message_id=error.args[0]))
	
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
				channel, message = await self.message_link_parser(message_link)
				
				if not channel.permissions_for(ctx.author).manage_messages:
					raise InvalidMessageLink(message_link)
				
				# message not pinned
				if not message.pinned:
					await pin_message(message, channel)
				
				await send_info(ctx, server.lang_request("info.message.pinned"))
			except InvalidMessageLink as error:
				await send_error(ctx, server.lang_request("error.invalid_argument.invalid_message_link").format(message_link=error.args[0]))
			except InvalidChannelID as error:
				await send_error(ctx, server.lang_request("error.invalid_argument.invalid_channel_id").format(channel_id=error.args[0]))
			except InvalidMessageID as error:
				await send_error(ctx, server.lang_request("error.invalid_argument.invalid_message_id").format(message_id=error.args[0]))
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
