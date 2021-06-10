from discord.ext.commands import Cog

import global_object
from global_object import Inited_cog, ready
from tools.load import load_internal, load_lang
from tools.setting import ServerSetting

class Event(Inited_cog):
	ready()
	
	@Cog.listener()
	async def on_ready(self):
		if not global_object.running:
			print(load_internal()["message"]["ready"])
			global_object.running = True
	
	@Cog.listener()
	async def on_member_join(self, member):
		server_id = member.guild.id
		member_join_message = ServerSetting(server_id).request("optional.member_join_message")
		
		if member_join_message["able"]:
			channel = self.bot.get_channel(member_join_message["channel"])
			await channel.send(load_lang(server_id, "message.member_join_message").format(member = member))
	
	@Cog.listener()
	async def on_member_leave(self, member):
		server_id = member.guild.id
		member_leave_message = ServerSetting(server_id).request("optional.member_leave_message")
		
		if member_leave_message["able"]:
			channel = self.bot.get_channel(member_leave_message["channel"])
			await channel.send(load_lang(server_id, "message.member_leave_message").format(member = member))

def setup(bot):
	bot.add_cog(Event(bot))
