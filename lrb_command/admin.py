from core import Server
from core.language import PUBLIC_LANGUAGE_DIR, language_support_check
from disnake.ext.commands import command, has_permissions
from disnake.role import Role
from exceptions import LanguageNotChange, LanguageNotSupport, PrefixNotChange, RoleNotChange

from utils.cog import InitedCog

@has_permissions(administrator=True)
class Admin(InitedCog):
	@command()
	async def set_lang(self, ctx, lang_code: str):
		if not language_support_check(PUBLIC_LANGUAGE_DIR):
			await self.send_error(ctx, "error.invalid_argument.lang_not_found")
		
		if not lang_code == self.get_server_data(ctx.guild.id)["lang_code"]:
			self.update_server(ctx.guild.id, {"lang_code": lang_code})
		
		await self.send_info(ctx, "info.server.set_lang", language=lang_code)
	
	@command()
	async def set_prefix(self, ctx, prefix):
		if not prefix == ctx.prefix:
			self.update_server(ctx.guild.id, {"prefix": prefix})
		await self.send_info(ctx, "info.server.set_prefix")
	
	@command()
	async def auto_role(self, ctx, *roles):
		auto_roles = self.get_server_data(ctx.guild.id)["auto_roles"]
		
		if not auto_roles == roles:
			self.update_server(ctx.guild.id, {"auto_roles": roles})
		await self.send_info(ctx, "info.server.set_auto_role", roles=", ".join(roles))
	
	@command(aliases=["del_mes", "del_msg", "purge"])
	async def delete_message(self, ctx, delete_num=1):
		await ctx.channel.purge(limit=delete_num + 1)
		await self.send_info(ctx, "info.message.deleted", deleted_number=delete_num)

def setup(bot):
	bot.add_cog(Admin(bot))
