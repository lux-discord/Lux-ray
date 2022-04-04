from disnake.ext.commands import command, has_guild_permissions

from core.cog import GeneralCog
from core.data import PrefixData
from core.language import GLOBAL_SUPPORT_LANGUAGE


@has_guild_permissions(administrator=True)
class Admin(GeneralCog):
	@command()
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
	async def set_prefix(self, ctx, prefix):
		server = await self.get_server(ctx.guild.id)
		
		if prefix == ctx.prefix:
			return await server.send_warning(ctx, "Prefix did not change")
		
		await self.update_prefix(PrefixData(_id=ctx.guild.id, prefix=prefix))
		await self.send_info(ctx, "Successful set prefix to `{prefix}`", prefix=prefix)
	
	@command()
	async def auto_role(self, ctx, *roles):
		server = await self.get_server(ctx.guild.id)
		
		if tuple(server.role["auto_role"]) == roles:
			return await server.send_warning(ctx, "Auto-role did not change")
		
		# Need improve
		new_role = server.role
		new_role["auto_role"] = roles
		update = server.update(role=new_role)
		await self.update_server(update)
		await self.send_info(ctx, "Successful set auto-role to {roles}", roles=", ".join(roles))
	
	@command(aliases=["del_mes", "del_msg", "purge"])
	async def delete_message(self, ctx, amount=1):
		await ctx.channel.purge(limit=amount+1)
		await self.send_info(ctx, "`{amount}` message(s) deleted", amount=amount)

def setup(bot):
	bot.add_cog(Admin(bot))
