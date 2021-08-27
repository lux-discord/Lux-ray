from core import InitedCog, Server
from discord.channel import TextChannel
from discord.errors import HTTPException
from discord.ext.commands.core import command, has_permissions
from discord.message import Message
from exceptions import InvalidChannelID, InvalidMessageID, InvalidMessageLink


@has_permissions(manage_messages=True)
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
	
	async def process_message_link(self, message_link, process, server: Server):
		try:
			channel, message = await self.message_link_parser(message_link)
			await process(channel, message)
		except InvalidMessageLink as error:
			await server.send_error("error.invalid_argument.invalid_message_link", message_link=error.args[0])
		except InvalidChannelID as error:
			await server.send_error("error.invalid_argument.invalid_channel_id", channel_id=error.args[0])
		except InvalidMessageID as error:
			await server.send_error("error.invalid_argument.invalid_message_id", message_id=error.args[0])
	
	@command()
	async def pin(self, ctx, message_link: str=None):
		ctx_message = ctx.message
		ctx_channel = ctx.channel
		server = Server(ctx)
		
		async def pin_message(ctx, message, channel):
			await message.pin(reason=server.lang_request("audit_log.reason.message.pin_message").format(
				user=f"{ctx.author.name}(ID: {ctx.author.id})",
				command_name=ctx.invoked_with)
			)
			
			async for message in channel.history(limit=7):
				if not message.content:
					await message.delete()
					break
		
		await ctx_message.delete()
		
		if message_link:
			async def process(channel: TextChannel, message: Message):
				if not channel.permissions_for(ctx.author).manage_messages:
					raise InvalidMessageLink(message_link)
				
				# message not pinned
				if not message.pinned:
					await pin_message(ctx, message, channel)
				
				await server.send_info("info.message.pinned")
			
			await self.process_message_link(message_link, process, server)
		elif refer_mes := ctx_message.reference:
			refer_mes = refer_mes.resolved
			
			if not refer_mes.pinned:
				await pin_message(ctx, refer_mes, ctx_channel)
			
			await server.send_info("info.message.pinned")
		else:
			async for message in ctx_channel.history(limit=1):
				if not message.pinned:
					await pin_message(ctx, message, ctx_channel)
			
			await server.send_info("info.message.pinned")
	
	@command()
	async def unpin(self, ctx, message_link: str=None):
		ctx_message = ctx.message
		ctx_channel = ctx.channel
		server = Server(ctx)
		
		async def unpin_message(ctx, message, channel):
			await message.unpin(reason=server.lang_request("audit_log.reason.message.unpin_message").format(
				user=f"{ctx.author.name}(ID: {ctx.author.id})",
				command_name=ctx.invoked_with)
			)
			
			# delete system message
			async for message in channel.history(limit=7):
				if not message.content:
					await message.delete()
					break
		
		await ctx_message.delete()
		
		if message_link:
			async def process(channel: TextChannel, message: Message):
				if not channel.permissions_for(ctx.author).manage_messages:
					raise InvalidMessageLink(message_link)
				
				if message.pinned:
					await unpin_message(ctx, message, channel)
				
				await server.send_info("info.message.unpinned")
			
			await self.process_message_link(message_link, process, server)
		elif refer_mes := ctx_message.reference:
			refer_mes = refer_mes.resolved
			
			if refer_mes.pinned:
				await unpin_message(ctx, refer_mes, ctx_channel)
			
			await server.send_info("info.message.unpinned")
		else:
			async for message in ctx_channel.history(limit=1):
				if message.pinned:
					await unpin_message(ctx, message, ctx_channel)
			
			await server.send_info("info.message.unpinned")
	
	@command(aliases=["del_mes", "del_msg", "purge"])
	async def delete_message(self, ctx, delete_num=1):
		await ctx.channel.purge(limit=delete_num + 1)
		await Server(ctx).send_info("info.message.deleted", deleted_number=delete_num)

def setup(bot):
	bot.add_cog(Messages(bot))
