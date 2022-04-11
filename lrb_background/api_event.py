#from disnake import Member
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
	async def on_message(self, message):
		if message.author.id == self.bot.user.id:
			return
		
		def keyword_reply(message_content: str):
			# Maybe will use command to set keyword and reply in future?
			keyword_to_reply = {
				"YABE": "https://tenor.com/view/shirakami-fubuki-hololive-yabe-vtuber-gif-19227770",
				"窩不知道": "https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1622039006854.jpg"
			}
			
			return keyword_to_reply[message_content] if message_content in keyword_to_reply else None
		
		if reply := keyword_reply(message.content):
			await message.channel.send(reply)
	
	"""
	# [Bug] bot won't recived event
	@Cog.listener()
	async def on_member_join(self, member: Member):
		server = await self.get_server(member.guild.id)
		
		if auto_roles := server.role["auto_role"]:
			roles = [member.guild.get_role(role_id) for role_id in auto_roles]
			await member.add_roles(*roles)
	"""

def setup(bot):
	bot.add_cog(ApiEvent(bot))
