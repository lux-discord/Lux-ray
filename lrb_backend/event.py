from discord.ext.commands import Cog

import global_object

from tools.load import load_internal
from tools.setting import ServerSetting
from tools.token import Token
from global_object import Inited_cog, ready

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
		server_setting = ServerSetting(server_id)
		member_join_message = server_setting.request(Token("optional.member_join_message"))
		
		if member_join_message["able"]:
			channel = self.bot.get_channel(member_join_message["channel"])
			await channel.send(server_setting.request_lang("message.member_join_message").format(member = member))
	
	@Cog.listener()
	async def on_member_leave(self, member):
		server_id = member.guild.id
		server_setting = ServerSetting(server_id)
		member_leave_message = server_setting.request(Token("optional.member_leave_message"))
		
		if member_leave_message["able"]:
			channel = self.bot.get_channel(member_leave_message["channel"])
			await channel.send(server_setting.request_lang("message.member_leave_message").format(member = member))

def setup(bot):
	bot.add_cog(Event(bot))
