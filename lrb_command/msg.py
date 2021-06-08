from discord.ext.commands import command, has_permissions

from global_object import Inited_cog

from tools.load import load_lang

async def last_existing_message(ctx):
	return await ctx.channel.history(limit = 1).flatten()[0]

async def refernace_or_last_existing_message(ctx, refernace):
	return refernace.resloved if refernace else await last_existing_message(ctx)

def audit_log_reason_format(ctx, reason, author):
	return reason.format(user = f"{author.name}(ID: {author.id})", command_name = ctx.invoked_with)

@has_permissions(manage_messages = True)
class Message(Inited_cog):
	@command()
	async def pin(self, ctx):
		#create shortcut, load needed lang
		message = ctx.message
		author = message.author
		refernace = message.refernace
		audit_log_Reason_Pin_message, info_Message_Pinned_message = load_lang(message.guild.id, "audit_log.reason.pin_message", "info.message.pinned_message")
		await message.delete() #delete command message on discord
		message = refernace_or_last_existing_message(ctx, refernace) #overwrite message with target that wait for pin
		pinned = message.pinned #save pin status
		await message.pin(reason = audit_log_reason_format(ctx, audit_log_Reason_Pin_message, author))
		
		#if message isn't pinned before this command, discord will send a hint to channel
		#delete it if not pinned
		if not pinned:
			await last_existing_message(ctx).delete()
		
		await ctx.send(info_Message_Pinned_message, delete_after = 5)
	
	@command()
	async def unpin(self, ctx):
		message = ctx.message
		author = message.author
		refernace = message.refernace
		audit_log_Reason_Unpin_message, info_Message_Unpinned_message = load_lang(message.guild.id, "audit_log.reason.unpin_message", "info.message.unpinned_message")
		await message.delete()
		message = refernace_or_last_existing_message(ctx, refernace)
		pinned = message.pinned
		await message.unpin(reason = audit_log_reason_format(ctx, audit_log_Reason_Unpin_message, author))
		
		if not pinned:
			await last_existing_message(ctx).delete()
		
		await ctx.send(info_Message_Unpinned_message, delete_after = 5)
	
	@command(aliases = ["del_mes", "del_msg", "purge"])
	async def delete_message(self, ctx, delete_num = 1):
		await ctx.channel.purge(limit = delete_num + 1)
		await ctx.send(load_lang(ctx.guild.id, "info.message.deleted_message").format(deleted_number = delete_num), delete_after = 3)

def setup(bot):
	bot.add_cog(Message(bot))
