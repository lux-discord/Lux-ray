from disnake import Member
from disnake.ext.commands.cog import Cog

from core.cog import GeneralCog


class ApiEvent(GeneralCog):
	@Cog.listener()
	async def on_connect(self):
		print("Connected to Discord")
	
	@Cog.listener()
	async def on_ready(self):
		print("Bot is ready")
	
	@Cog.listener()
	async def on_member_join(self, member: Member):
		# [Bug] bot won't recived event
		server = await self.get_server(member.guild.id)
		
		if auto_roles := server.role["auto_role"]:
			roles = [member.guild.get_role(role_id) for role_id in auto_roles]
			await member.add_roles(*roles)

def setup(bot):
	bot.add_cog(ApiEvent(bot))
