from discord.ext.commands import command, is_owner

from cog import cog_folder_abbr_to_fullname, cog_folder_dict_generater
from global_object import Inited_cog

from tools.load import load_lang
from tools.prefix import save_prefixes

async def cog_action_looper(ctx, cog_folder, action, action_message: str, *cogs):
	cog_list = cog_folder_dict_generater(cog_folder_abbr_to_fullname[cog_folder])
	
	for cog in cogs:
		action(cog_list[cog])
		await ctx.send(action_message.format(cog_name = cog))

@is_owner()
class Dev(Inited_cog):
	@command()
	async def load_cmd(self, ctx, *command_cogs):
		loaded_cmd = load_lang(ctx.guild.id, "info.command.loaded_cmd")
		
		await cog_action_looper(ctx, "cmd", self.bot.load_extension, loaded_cmd, *command_cogs)
	
	@command()
	async def unload_cmd(self, ctx, *command_cogs):
		unloaded_cmd = load_lang(ctx.guild.id, "info.command.unloaded_cmd")
		
		await cog_action_looper(ctx ,"cmd", self.bot.unload_extension, unloaded_cmd, *command_cogs)
	
	@command()
	async def reload_cmd(self, ctx, *command_cogs):
		reloaded_cmd = load_lang(ctx.guild.id, "info.command.reloaded_cmd")
		
		await cog_action_looper(ctx, "cmd", self.bot.reload_extension, reloaded_cmd, *command_cogs)
	
	@command()
	async def reload_all_cmd(self, ctx):
		reloaded_all_cmd = load_lang(ctx.guild.id, "info.command.reloaded_all_cmd")
		cmd_cog_list = cog_folder_dict_generater(cog_folder_abbr_to_fullname["cmd"])
		
		await cog_action_looper(ctx, "cmd", self.bot.reload_extension, reloaded_all_cmd, cmd_cog_list)
	
	@command()
	async def save(self, ctx):
		save_prefixes()

def setup(bot):
	bot.add_cog(Dev(bot))
