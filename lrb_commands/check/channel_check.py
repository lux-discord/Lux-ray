import discord
from discord.ext import commands
import json

with open('setting/setting_global.json', 'r', encoding = 'UTF-8') as setting_file:
	setting = json.load(setting_file)
with open(f'lang/{setting["lang"]}.json', 'r', encoding = 'UTF-8') as lang_file:
	lang = json.load(lang_file)

def in_channel(channel):
	def predicate(ctx):
		pass #return ctx.channel.id == setting[]
	return commands.check(predicate)