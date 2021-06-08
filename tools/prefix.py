from global_object import stable

from tools.json_open import json_load, json_dump
from tools.run_here import run_here

prefixes_file_path = "../prefixes.json"

@run_here
def load_prefixes():
	global prefixes
	prefixes = json_load(prefixes_file_path)
	
def get_prefix(bot, message):
	server_id = message.guild.id
	default_prefix = {
		"main": "lr",
		"indev": "rl"
	}
	prefix = prefixes.setdefault(server_id, default_prefix)
	prefix = prefix["main" if stable else "indev"]
	
	return prefix + " ", prefix

def request_prefix(server_id):
	return prefixes[server_id]["main" if stable else "indev"]

def edit_prefix(server_id, prefix):
	global prefixes
	
	prefixes[server_id]["main" if stable else "indev"] = prefix
	
	save_prefixes()

@run_here
def save_prefixes():
	global prefixes
	json_dump(prefixes, prefixes_file_path)
