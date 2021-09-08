from core import InitedCog, Server
from discord import Message
from discord.ext.commands import command, has_permissions
from exceptions import InvalidArgument
from utils.message import target_message


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
			async for message in message.channel.history(limit=5):
				if not message.content:
					await message.delete()
					break
			
			await server.send_info("info.message.pinned")
		
		await ctx_message.delete()
		
		try:
			async with target_message(ctx, message_link=message_link, manage_messages=True) as message:
				await pin_message(message)
		except InvalidArgument as error:
			await server.send_error("error.invalid_argument.invalid_message_link", message_link=error.args[0])
	
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
			async for message in message.channel.history(limit=5):
				if not message.content:
					await message.delete()
					break
			
			await server.send_info("info.message.unpinned")
		
		await ctx_message.delete()
		
		try:
			async with target_message(ctx, message_link=message_link, manage_messages=True) as message:
				await unpin_message(message)
		except InvalidArgument as error:
			await server.send_error("error.invalid_argument.invalid_message_link", message_link=error.args[0])
	
	@command(aliases=["mes_link", "msg_link"])
	async def message_link(self, ctx):
		async with target_message(ctx) as message:
			return await ctx.send(message.jump_url)

def setup(bot):
	bot.add_cog(Messages(bot))
