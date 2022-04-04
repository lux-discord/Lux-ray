from disnake import Message
from disnake.ext.commands import command, has_permissions
from utils.message import target_message
from core.cog import GeneralCog

@has_permissions(manage_messages=True)
class Messages(GeneralCog):
	@staticmethod
	async def delete_system_message(channel):
		async for message in channel.history(limit=5):
			if message.is_system():
				await message.delete()
				break
	
	@command()
	async def pin(self, ctx):
		await ctx.message.delete()
		server = await self.get_server(ctx.guild.id)
		
		async def do_pin(message: Message):
			reason = server.translate("User `{user_name_with_id}` used command `{command_name}`").format(
				user_name_with_id=f"{ctx.author.name}(ID: {ctx.author.id})",
				command_name=ctx.invoked_with
			)
			
			await message.pin(reason=reason)
			await self.delete_system_message(message.channel)
			await server.send_info(ctx, "Successful pinning message")
		
		async with target_message(ctx) as message:
			if message.pinned:
				return await server.send_warning(ctx, "Message pinned")
			await do_pin(message)
	
	@command()
	async def unpin(self, ctx):
		await ctx.message.delete()
		server = await self.get_server(ctx.guild.id)
		
		async def unpin_message(message: Message):
			reason = server.translate("User `{user_name_with_id}` used command `{command_name}`").format(
				user_name_with_id=f"{ctx.author.name}(ID: {ctx.author.id})",
				command_name=ctx.invoked_with
			)
			await message.unpin(reason=reason)
			await self.delete_system_message(message.channel)
			await server.send_info(ctx, "Successful unpinning message")
		
		async with target_message(ctx) as message:
			if not message.pinned:
				return await server.send_warning(ctx, "Message not pinned")
			await unpin_message(message)
	
	@command(aliases=["mes_link", "msg_link"])
	async def message_link(self, ctx):
		async with target_message(ctx) as message:
			return await ctx.send(message.jump_url)

def setup(bot):
	bot.add_cog(Messages(bot))
