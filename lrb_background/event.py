import discord
from discord.ext import commands

from tools import server_setting, load_lang

class Event(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.running = False
	
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
		if not self.running:
			print(load_lang('internal', 'bot_ready').format(bot_name = str(self.bot.user)[:-5]))
		
		self.running = True

def setup(bot):
	bot.add_cog(Event(bot))