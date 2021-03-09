import discord
from discord.ext import commands
import json
import os

def generate_server_setting(server_id):
	os.mkdir(f'setting/server_{server_id}')
	with open('setting/default_server_setting.json', 'r', encoding = 'UTF-8') as default_setting_file:
		with open(f'setting/server_{server_id}/setting.json', 'w', encoding = 'UTF-8') as setting_file:
			setting_file.write(default_setting_file.read())

def generate_server_user_setting(ctx):
	with open('setting/default_user_setting.json', 'r', encoding = 'UTF-8') as default_setting_file:
		with open(f'setting/server_{ctx.guild.id}/user_{ctx.author.id}.json', 'w', encoding = 'UTF-8') as setting_file:
			setting_file.write(default_setting_file.read())

def get_server_setting(server_id: int):
	if not os.path.exists(f'setting/server_{server_id}'):
		generate_server_setting(server_id)
	
	with open(f'setting/server_{server_id}/setting.json', 'r', encoding = 'UTF-8') as setting_file:
		setting = json.load(setting_file)

	return setting

def get_server_user_setting(ctx):
	if not os.path.exists(f'setting/server_{ctx.guild.id}'):
		generate_server_setting(ctx.guild.id)
	
	if not os.path.exists(f'setting/server_{ctx.guild.id}/user_{ctx.author.id}.json'):
		generate_server_user_setting(ctx)
	
	with open(f'setting/server_{ctx.guild.id}/user_{ctx.author.id}.json', 'r', encoding = 'UTF-8') as setting_file:
		setting = json.load(setting_file)
	
	return setting