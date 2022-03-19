from core.language import GLOBAL_SUPPORT_LANGUAGE
from disnake.ext.commands import command, has_guild_permissions

from core.cog import GeneralCog

@has_guild_permissions(administrator=True)
class Admin(GeneralCog):
	@command()
	async def set_lang(self, ctx, lang_code: str):
		if lang_code not in GLOBAL_SUPPORT_LANGUAGE:
			await self.send_error(ctx, self.token("error.invalid_argument.lang_not_found"))
		
		if lang_code != self.get_server_data(ctx.guild.id)["lang_code"]:
			self.update_server(ctx.guild.id, {"lang_code": lang_code})
		
		await self.send_info(ctx, self.token("info.server.set_lang"), language=lang_code)
	
	@command()
	async def set_prefix(self, ctx, prefix):
		if prefix != ctx.prefix:
			self.update_server(ctx.guild.id, {"prefix": prefix})
		
		await self.send_info(ctx, "info.server.set_prefix")
	
	@command()
	async def auto_role(self, ctx, *roles):
		auto_roles = self.get_server_data(ctx.guild.id)["auto_roles"]
		
		if not auto_roles == roles:
			self.update_server(ctx.guild.id, {"auto_roles": roles})
		await self.send_info(ctx, self.token("info.server.set_auto_role"), roles=", ".join(roles))
	
	@command(aliases=["del_mes", "del_msg", "purge"])
	async def delete_message(self, ctx, delete_num=1):
		await ctx.channel.purge(limit=delete_num+1)
		await self.send_info(ctx, self.token("info.message.deleted"), deleted_number=delete_num)

def setup(bot):
	bot.add_cog(Admin(bot))
