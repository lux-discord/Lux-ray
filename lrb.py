import discord
from discord.ext import commands
import json
import os
from config import load_config

#dev setting
indev = True

if indev:
	prefix_use = 'prefix_dev'
	token_use = 'token_dev'
else:
	import keep_alive
	prefix_use = 'prefix'
	token_use = 'token'

#bot setting
print("Setting bot parameters...")

def get_prefix(client, message):
	server_setting_path = f"settings/server/{message.guild.id}.json"
	default_server_setting_path = "settings/default_server_setting.json"
	
	try:
		with open(server_setting_path, 'r', encoding = 'UTF-8') as server_setting:
			prefix = json.load(server_setting)['config'][prefix_use]
			return prefix + ' '
	except FileNotFoundError:
		with open(default_server_setting_path, 'r', encoding = 'UTF-8') as default_server_setting:
			default_server_setting = json.load(default_server_setting)
			prefix = default_server_setting[prefix_use]
			
			with open(server_setting_path, 'w', encoding = 'UTF-8') as server_setting:
				json.dump(default_server_setting , server_setting, indent = '\t')
			
			return prefix + ' ', prefix

owner_id, token = load_config('owner_id', token_use)
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
lrb = commands.Bot(command_prefix = get_prefix, owner_id = int(owner_id), intents = intents)
setattr(lrb, 'indev', indev)

#load ext
print("Loading extensions...")

for folder in os.listdir('.'):
	if os.path.isdir(folder) and folder.startswith('lrb'):
		print(f"  {folder}")
		
		for file in os.listdir(folder):
			if os.path.isfile and file.endswith('.py'):
				file = file[:-3]
				
				print(f"    {file}")
				
				lrb.load_extension(f"{folder}.{file}")

#start run
if __name__ == '__main__':
	print("Starting bot")
	
	if not indev:
		keep_alive.keep_alive()
	
	lrb.run(token)
