from core import InitedCog
from core.db import server_coll
from discord import Member
from discord.ext.commands.cog import Cog
from discord.utils import get


class Event(InitedCog):
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
			server_data: dict = server_coll.find_one({"server_id": member.guild.id})
			auto_roles: list = server_data["roles"]["auto_roles"]
			
			if auto_roles:
				_ = [await member.add_roles(get(member.guild.roles, name=role)) for role in auto_roles]
		
		await auto_role()

def setup(bot):
	bot.add_cog(Event(bot))
