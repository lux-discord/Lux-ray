from basic_import import *
from basic_cmd_import import *

from tools.server_setting import server_setting

class Event(Inited_cog):
	@commands.Cog.listener()
	async def on_member_join(self, member):
		ss = server_setting(member.guild.id)
		
		if ss['config']['member_join_message']:
			channel = self.bot.get_channel(server_setting['channel']['member_join_message'])
			await channel.send(f'{member} has join to this server')
	
	@commands.Cog.listener()
	async def on_member_leave(self, member):
		ss = server_setting(member.guild.id)
		
		if ss['config']['member_leave_message']:
			channel = self.bot.get_channel(server_setting['channel']['member_leave_message'])
			await channel.send(f'{member} has leave this server')
		
	@commands.Cog.listener()
	async def on_ready(self):
		ready_message = load_lang('internal')['bot_ready'].format(bot_name = str(self.bot.user)[:-5])
		print(ready_message)

def setup(bot):
	bot.add_cog(Event(bot))