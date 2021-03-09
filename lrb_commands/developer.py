import os

from basic_import import *
from basic_cmd_import import *

@commands.is_owner()
class Developer(Inited_cog):
	def __init__(self, bot):
		self.bot = bot
		self.file_list = [f"{folder}.{file[:-3]}" for folder in os.listdir() if folder.startswith('lrb_') for file in os.listdir(folder) if file.endswith('.py')]
			
	@commands.command()
	async def load(self, ctx, *extension_name):
		for ext_name in extension_name:
			for file in self.file_list:
				if ext_name in file:
					self.bot.load_extension(file)
					await ctx.send(load_lang(ctx.guild.id)['action']['loaded_ext'].format(extension_name = f"'{ext_name}'"))
	
	@commands.command()
	async def unload(self, ctx, *extension_name):
		for ext_name in extension_name:
			for file in self.file_list:
				if ext_name in file:
					self.bot.unload_extension(file)
					await ctx.send(load_lang(ctx.guild.id)['action']['unloaded_ext'].format(extension_name = f"'{ext_name}'"))
	
	@commands.command()
	async def reload(self, ctx, *extension_name):
		for ext_name in extension_name:
			for file in self.file_list:
				if ext_name in file:
					self.bot.reload_extension(file)
					await ctx.send(load_lang(ctx.guild.id)['action']['reloaded_ext'].format(extension_name = f"'{ext_name}'"))
	
	@commands.command()
	async def reload_all(self, ctx):
		for file in self.file_list:
			self.bot.reload_extension(file)

def setup(bot):
	bot.add_cog(Developer(bot))