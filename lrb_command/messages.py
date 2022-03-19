from disnake import Message
from disnake.ext.commands import command, has_permissions
from exceptions import InvalidUserInput
from utils.message import target_message
from core.cog import GeneralCog

@has_permissions(manage_messages=True)
class Messages(GeneralCog):
	async def delete_system_message(self, channel):
		async for message in channel.history(limit=5):
			if message.is_system():
				await message.delete()
				break
	
	@command()
	async def pin(self, ctx, message_link: str=None):
		async def pin_message(message: Message):
			reason = self.request_message(ctx.guild.id, "audit_log.reason.message.pin_message").format(
				user=f"{ctx.author.name}(ID: {ctx.author.id})",
				command_name=ctx.invoked_with
			)
			
			await message.pin(reason=reason)
			await message.pin(reason=self.request_message(ctx.guild.id, "audit_log.reason.message.pin_message").format(
				user=f"{ctx.author.name}(ID: {ctx.author.id})",
				command_name=ctx.invoked_with))
			
			# delete system message
			async for message in message.channel.history(limit=5):
				if not message.content:
					await message.delete()
					break
			
			await self.send_info(ctx, "info.message.pinned")
		
		await ctx.message.delete()
		
		try:
			async with target_message(ctx, message_link=message_link, manage_messages=True) as message:
				await pin_message(message)
		except InvalidUserInput as error:
			await self.send_error(ctx, "error.invalid_argument.invalid_message_link", message_link=error.args[0])
	
	@command()
	async def unpin(self, ctx, message_link: str=None):
		async def unpin_message(message: Message):
			await message.unpin(reason=self.request_message(ctx.guild.id, "audit_log.reason.message.unpin_message",
				user=f"{ctx.author.name}(ID: {ctx.author.id})",
				command_name=ctx.invoked_with))
			await self.delete_system_message(message.channel)
			await self.send_info(ctx, "info.message.unpinned")
		
		await ctx.message.delete()
		
		try:
			async with target_message(ctx, message_link=message_link, manage_messages=True) as message:
				await unpin_message(message)
		except InvalidUserInput as error:
			await self.send_error(ctx, "error.invalid_argument.invalid_message_link", message_link=error.args[0])
	
	@command(aliases=["mes_link", "msg_link"])
	async def message_link(self, ctx):
		async with target_message(ctx) as message:
			return await ctx.send(message.jump_url)

def setup(bot):
	bot.add_cog(Messages(bot))
