import os

import discord
from discord.ext import commands

from tools import load_lang
from tools.dev import sync_server_setting_to_default

@commands.is_owner()
class Developer(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.ext_name_path_dict = {file[:-3]: f"{folder}.{file[:-3]}" for folder in os.listdir() if folder.startswith('lrb_') for file in os.listdir(folder) if file.endswith('.py')}
	
	@commands.command()
	async def load(self, ctx, *extensions):
		loaded_extension = load_lang(ctx.guild.id, 'action.loaded_ext')
		
		for extension in extensions:
			if extension in self.ext_name_path_dict:
				self.bot.load_extension(self.ext_name_path_dict[extension])
				await ctx.send(loaded_extension.format(extension_name = f"'{extension}'"))
	
	@commands.command()
	async def unload(self, ctx, *extensions):
		unload_extension = load_lang(ctx.guild.id, 'action.unloaded_ext')
		
		for extension in extensions:
			if extension in self.ext_name_path_dict:
				self.bot.unload_extension(self.ext_name_path_dict[extension])
				await ctx.send(unload_extension.format(extension_name = f"'{extension}'"))
	
	@commands.command()
	async def reload(self, ctx, *extensions):
		reloaded_all_ext, reloaded_ext = load_lang(ctx.guild.id, 'action.reloaded_all_ext', 'action.reloaded_ext')
		
		if len(extensions) == 1 and extensions[0] == 'all':
			for extension_path in self.ext_name_path_dict.values():
				self.bot.reload_extension(extension_path)
			await ctx.send(reloaded_all_ext)
			return
		
		for extension in extensions:
			if extension in self.ext_name_path_dict:
				self.bot.reload_extension(self.ext_name_path_dict[extension])
				await ctx.send(reloaded_ext.format(extension_name = f"'{extension}'"))
	
	@commands.command()
	async def server_setting(self, ctx, option, *option_args):
		guild_id = ctx.guild.id
		options = {
			'sync_to_default': sync_server_setting_to_default
		}
		options_mes = {
			'sync_to_default': 'action.sync_server_setting_to_default'
		}
		
		if option not in options:
			await ctx.send(load_lang(guild_id, 'error.option_not_found').format(option = option))
			return
		
		options[option](*option_args)
		await ctx.send(load_lang(guild_id, options_mes[option]))

def setup(bot):
	bot.add_cog(Developer(bot))
