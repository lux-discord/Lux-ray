from discord.ext.commands import command, has_permissions

from global_object import Inited_cog
from language.language import languages
from tools.load import load_lang
from tools.prefix import request_prefix, edit_prefix
from tools.setting import ServerSetting


@has_permissions(administrator = True)
class Server(Inited_cog):
	@command()
	async def set_lang(self, ctx, language):
		server_id = ctx.guild.id
		server_setting = ServerSetting(server_id)
		
		if language not in languages:
			return await ctx.send(load_lang(server_id, "error.lang_not_found"))
		
		server_lang = server_setting.request("config.language")
		
		if language == server_lang:
			return await ctx.send(load_lang(server_id, "error.lang_not_change"))
		
		server_setting.edit({"config.language": language})
		await ctx.send(load_lang(server_id, "info.server.set_lang").format(language = languages[language]))
	
	@command()
	async def set_prefix(self, ctx, prefix):
		server_id = ctx.guild.id
		server_prefix = request_prefix(server_id)
		
		if prefix == server_prefix:
			return await ctx.send(load_lang(server_id, "error.prefix_not_change"))
		
		edit_prefix(server_id, prefix)
		await ctx.send(load_lang(server_id, "info.server.set_prefix"))

def setup(bot):
	bot.add_cog(Server(bot))
