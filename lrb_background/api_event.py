from disnake import Member
from disnake.ext.commands.cog import Cog
from disnake.utils import get

from core.cog import GeneralCog


class ApiEvent(GeneralCog):
	@Cog.listener()
	async def on_ready(self):
		print("Bot is ready")
	
	@Cog.listener()
	async def on_member_join(self, member: Member):
		async def auto_role():
			server_data: dict = self.db.find_one({"_id": member.guild.id})
			
			if auto_roles := server_data["roles"]["auto_roles"]:
				server_roles = member.guild.roles
				_ = [await member.add_roles(get(server_roles, name=role)) for role in auto_roles]
		
		await auto_role()

def setup(bot):
	bot.add_cog(ApiEvent(bot))
