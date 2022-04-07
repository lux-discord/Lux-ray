from disnake.ext.commands import command, has_guild_permissions
from disnake.role import Role

from core.cog import GeneralCog
from core.data import PrefixData
from core.language import GLOBAL_SUPPORT_LANGUAGE


class Admin(GeneralCog):
	@command()
	@has_guild_permissions(administrator=True)
	async def set_lang(self, ctx, lang_code: str):
		server = await self.get_server(ctx.guild.id)
		
		if lang_code not in GLOBAL_SUPPORT_LANGUAGE:
			return await server.send_error(ctx, "Language code `{lang_code}` is not support", lang_code=lang_code)
		
		if server.lang_code == lang_code:
			return await server.send_warning(ctx, "Language did not change")
		
		update = server.update(lang_code=lang_code)
		await self.update_server(update)
		await server.send_info(ctx, "Successful set language to `{lang_code}`", lang_code=lang_code)
	
	@command()
	@has_guild_permissions(administrator=True)
	async def set_prefix(self, ctx, prefix):
		server = await self.get_server(ctx.guild.id)
		
		if prefix == ctx.prefix:
			return await server.send_warning(ctx, "Prefix did not change")
		
		await self.update_prefix(PrefixData(_id=ctx.guild.id, prefix=prefix))
		await self.send_info(ctx, "Successful set prefix to `{prefix}`", prefix=prefix)
	
	@command()
	@has_guild_permissions(administrator=True)
	async def auto_role(self, ctx, *roles: Role):
		server = await self.get_server(ctx.guild.id)
		
		if not roles:
			server.role["auto_role"] = []
			update = server.update(role=server.role)
			await self.update_server(update)
			return await server.send_info(ctx, "Auto-roles cleared")
		
		role_ids = {role.id for role in roles}
		
		if set(server.role["auto_role"]) == role_ids:
			return await server.send_warning(ctx, "Auto-role did not change")
		
		# Need improve
		server.role["auto_role"] = list(role_ids)
		update = server.update(role=server.role)
		await self.update_server(update)
		await self.send_info(ctx, "Successful set auto-role to {roles}", roles=", ".join(role.name for role in roles))

def setup(bot):
	bot.add_cog(Admin(bot))
