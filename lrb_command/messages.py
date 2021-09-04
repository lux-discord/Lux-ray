from core import InitedCog, Server
from discord import Message
from discord.ext.commands import command, has_permissions
from exceptions import InvalidArgument, InvalidMessageLink
from tool.message import parse_message_link, get_last_exist_message


@has_permissions(manage_messages=True)
class Messages(InitedCog):
	@command()
	async def pin(self, ctx, message_link: str=None):
		ctx_message = ctx.message
		server = Server(ctx)
		
		async def pin_message(message: Message):
			await message.pin(reason=server.lang_request("audit_log.reason.message.pin_message").format(
				user=f"{ctx.author.name}(ID: {ctx.author.id})",
				command_name=ctx.invoked_with)
			)
			
			# delete system message
			async for message in message.channel.history(limit=7):
				if not message.content:
					await message.delete()
					break
			
			await server.send_info("info.message.pinned")
		
		await ctx_message.delete()
		
		if message_link:
			try:
				message: Message = await parse_message_link(self.bot, message_link)
				
				if not message.channel.permissions_for(ctx.author).manage_messages:
					raise InvalidMessageLink(message_link)
				
				await pin_message(message)
			except InvalidArgument as error:
				await server.send_error("error.invalid_argument.invalid_message_link", message_link=error.args[0])
		elif refer_mes := ctx_message.reference:
			await pin_message(refer_mes.resolved)
		else:
			await pin_message(await get_last_exist_message(ctx.channel))
	
	@command()
	async def unpin(self, ctx, message_link: str=None):
		ctx_message = ctx.message
		server = Server(ctx)
		
		async def unpin_message(message: Message):
			await message.unpin(reason=server.lang_request("audit_log.reason.message.unpin_message").format(
				user=f"{ctx.author.name}(ID: {ctx.author.id})",
				command_name=ctx.invoked_with)
			)
			
			# delete system message
			async for message in message.channel.history(limit=7):
				if not message.content:
					await message.delete()
					break
			
			await server.send_info("info.message.unpinned")
		
		await ctx_message.delete()
		
		if message_link:
			try:
				message: Message = await parse_message_link(self.bot, message_link)
				
				if not message.channel.permissions_for(ctx.author).manage_messages:
					raise InvalidMessageLink(message_link)
				
				await unpin_message(message)
			except InvalidArgument as error:
				await server.send_error("error.invalid_argument.invalid_message_link", message_link=error.args[0])
		elif refer_mes := ctx_message.reference:
			await unpin_message(refer_mes.resolved)
		else:
			await unpin_message(await get_last_exist_message(ctx.channel))
	
	@command(aliases=["mes_link", "msg_link"])
	async def message_link(self, ctx):
		if refer_mes := ctx.message.reference:
			return await ctx.send(refer_mes.jump_url)
		await Server(ctx).send_error("error.target_not_found.no_reference_message")

def setup(bot):
	bot.add_cog(Messages(bot))
