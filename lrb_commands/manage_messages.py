import discord
from discord.ext import commands

from inited_cog import Inited_cog

from tools import load_lang

async def fetch_message_and_check_permission(ctx, positions: list):
	if ctx.guild.id != int(positions[0]):
		await ctx.send(lang['error']['invalid_server_id'], delete_after = 5)
		return
	if int(positions[1]) not in [channel.id for channel in ctx.guild.text_channels]:
		await ctx.send(lang['error']['invalid_channel_id'], delete_after = 5)
		return
	if not ctx.author.permissions_in(ctx.guild.get_channel(int(positions[1]))):
		await ctx.send(lang['error']['permission_too_low'].format(permission_name = lang['permission']['manage_messages']), delete_after = 5)
		return
	
	try:
		return await ctx.fetch_message(positions[2])
	except:
		await ctx.send(lang['error']['invalid_message_id'], delete_after = 5)
		return

class Manage_messages(Inited_cog):
	@commands.command()
	@commands.has_permissions(manage_messages = True)
	async def pin(self, ctx, link = None):
		await ctx.message.delete()
		if link == None:
			message = await ctx.channel.history(limit = 1).flatten()
			status = message[0].pinned
			await message[0].pin(reason = lang['reason']['pinned_message'].format(user_name = f'{ctx.author.name}(ID:{ctx.author.id})', command_name = ctx.invoked_with))
			if status == False:
				message = await ctx.channel.history(limit = 1).flatten()
				await message[0].delete()
			await ctx.send(lang['info']['pinned_message'], delete_after = 3)
		else:
			if lang['message_base_link'] in link:
				message_positions = link[len(lang['message_base_link']):].split('/')
				message = await fetch_message_and_check_permission(ctx, message_positions)
				if message == None:
					pass
				else:
					status = message.pinned
					await message.pin(reason = lang['reason']['pinned_message'].format(user_name = f'{ctx.author.name}(ID:{ctx.author.id})', command_name = ctx.invoked_with))
					if status == False:
						channel = ctx.guild.get_channel(int(message_positions[1]))
						message = await channel.history(limit = 1).flatten()
						await message[0].delete()
					await ctx.send(lang['info']['pinned_message'], delete_after = 3)
			else:
				await ctx.send(lang['error']['invalid_link'], delete_after = 5)
	
	@commands.command()
	@commands.has_permissions(manage_messages = True)
	async def unpin(self, ctx, link = None):
		await ctx.message.delete()
		if link == None:
			message = await ctx.channel.history(limit = 1).flatten()
			await message[0].unpin(reason = lang['reason']['unpinned_message'].format(user_name = f'{ctx.author.name}(ID:{ctx.author.id})', command_name = ctx.invoked_with))
			await ctx.send(lang['info']['unpinned_message'], delete_after = 3)
		else:
			if lang['message_base_link'] in link:
				message_positions = link[len(lang['message_base_link']):].split('/')
				message = await fetch_message_and_check_permission(ctx, message_positions)
				if message == None:
					pass
				else:
					await message.unpin(reason = lang['reason']['unpinned_message'].format(user_name = f'{ctx.author.name}(ID:{ctx.author.id})', command_name = ctx.invoked_with))
					await ctx.send(lang['info']['unpinned_message'], delete_after = 3)
			else:
				await ctx.send(lang['error']['invalid_link'], delete_after = 5)
	
	@commands.command()
	@commands.has_permissions(manage_messages = True)
	async def delete_message(self, ctx, num: int):
		guild_id = ctx.guild.id
		
		await ctx.channel.purge(limit = num+1)
		await ctx.send(load_lang(guild_id, "info.success_del_mes").format(num = str(num)), delete_after = 3)

def setup(bot):
	bot.add_cog(Manage_messages(bot))