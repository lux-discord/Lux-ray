from disnake import Member
from disnake.ext.commands.cog import Cog
from disnake.utils import get

from core.cog import GeneralCog


class ApiEvent(GeneralCog):
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.is_running:
			self.bot.is_running = True
			print("Bot is ready")
		else:
			print("Reconnected")
	
	@Cog.listener()
	async def on_member_join(self, member: Member):
		async def auto_role():
			server_data: dict = self.bot.db.find_one({"_id": member.guild.id})
			auto_roles: list = server_data["roles"]["auto_roles"]
			
			if auto_roles:
				server_roles = member.guild.roles
				_ = [await member.add_roles(get(server_roles, name=role)) for role in auto_roles]
		
		await auto_role()

def setup(bot):
	bot.add_cog(ApiEvent(bot))
