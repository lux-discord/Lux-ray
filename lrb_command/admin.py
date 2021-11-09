from core import Server
from core.language import SUPPORT_LANGUAGE
from disnake.ext.commands import command, has_guild_permissions
from disnake.role import Role
from exceptions import LanguageNotChange, LanguageNotSupport, PrefixNotChange, RoleNotChange

from utils.cog import InitedCog

@has_guild_permissions(administrator=True)
class Admin(InitedCog):
	@command()
	async def lang(self, ctx, language: str):
		server = Server(ctx)
		
		try:
			server.update_lang(language)
			await ctx.send(server.lang_request("info.server.set_lang").format(language=SUPPORT_LANGUAGE[language]))
		except LanguageNotChange:
			await ctx.send(server.lang_request("warning.value_not_change.lang"))
		except LanguageNotSupport:
			await ctx.send(server.lang_request("error.invalid_argument.lang_not_found"))
	
	@command()
	async def prefix(self, ctx, prefix):
		server = Server(ctx)
		
		try:
			server.update_prefix(self.bot.status, prefix)
			await ctx.send(server.lang_request("info.server.set_prefix"))
		except PrefixNotChange:
			await ctx.send(server.lang_request("warning.value_not_change.prefix"))
	
	@command()
	async def auto_role(self, ctx, *roles: Role):
		server = Server(ctx)
		auto_rules = [role.name for role in roles]
		
		try:
			server.update_auto_role(auto_rules)
			await ctx.send(server.lang_request("info.server.set_auto_role").format(roles=", ".join(auto_rules)))
		except RoleNotChange:
			await ctx.send(server.lang_request("warning.value_not_change.role"))
	
	@command(aliases=["del_mes", "del_msg", "purge"])
	async def delete_message(self, ctx, delete_num=1):
		await ctx.channel.purge(limit=delete_num + 1)
		await Server(ctx).send_info("info.message.deleted", deleted_number=delete_num)
	
	@command()
	async def role_permission_check(self, ctx):
		pass

def setup(bot):
	bot.add_cog(Admin(bot))
