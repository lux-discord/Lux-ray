from core import InitedCog, Server
from core.language import SUPPORT_LANGUAGE
from discord.ext.commands import command, has_guild_permissions
from discord.role import Role
from exceptions import LanguageNotChange, LanguageNotSupport, PrefixNotChange, RoleNotChange


@has_guild_permissions(administrator=True)
class Admin(InitedCog):
	@command()
	async def lang(self, ctx, language: str):
		server = Server(ctx)
		
		try:
			server.update_lang(language)
			await ctx.send(server.lang_request("info.server.set_lang").format(language=SUPPORT_LANGUAGE[language]))
		except LanguageNotChange:
			await ctx.send(server.lang_request("warning.value_not_change.lang_not_change"))
		except LanguageNotSupport:
			await ctx.send(server.lang_request("error.lang.lang_not_found"))
	
	@command()
	async def prefix(self, ctx, prefix):
		server = Server(ctx)
		
		try:
			server.update_prefix(self.bot.status, prefix)
			await ctx.send(server.lang_request("info.server.set_prefix"))
		except PrefixNotChange:
			await ctx.send(server.lang_request("error.prefix.prefix_not_change"))
	
	@command()
	async def auto_role(self, ctx, *roles):
		server = Server(ctx)
		guild_roles = ctx.guild.roles
		role_name_to_id = {role.name: role.id for role in guild_roles}
		auto_rules = []
		
		# type and exist check
		for role in roles:
			if role_type := type(role) not in {str, Role}:
				raise TypeError(f"role in rules must be str or discord.role.Role, not {role_type}")
			
			role_name = role if role_type is str else role.name
			
			if role_name not in role_name_to_id:
				return await ctx.send(server.lang_request("error.role.role_not_found").format(role_name=role_name))
			auto_rules.append(role_name_to_id[role_name])
		
		try:
			server.update_auto_role(*auto_rules)
			await ctx.send(server.lang_request("info.server.set_auto_role").format(roles=", ".join(auto_rules)))
		except RoleNotChange:
			await ctx.send(server.lang_request("error.role.role_not_change"))

def setup(bot):
	bot.add_cog(Admin(bot))
