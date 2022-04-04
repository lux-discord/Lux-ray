from disnake import Member
from disnake.ext.commands.cog import Cog
from disnake.utils import get

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
		async def auto_role():
			server = await self.get_server(member.guild.id)
			
			if server.role["auto_role"]:
				server_roles = member.guild.roles
				_ = [await member.add_roles(get(server_roles, name=role)) for role in auto_roles]
		
		await auto_role()

def setup(bot):
	bot.add_cog(ApiEvent(bot))
