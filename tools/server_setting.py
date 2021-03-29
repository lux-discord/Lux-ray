from json import load, dump

from .run_here import run_here

__all__ = [
	'load_server_setting',
	'request_server_setting',
	'overwrite_server_setting',
	'update_server_setting'
]

@run_here('..')
def load_server_setting(server_id, *key):
	if server_id == 'default':
		with open('settings/default_server_setting.json', 'r', encoding = 'UTF-8') as default_server_setting_file:
			return load(default_server_setting_file)
	
	server_setting_file_path = f"settings/server/{server_id}.json"
	
	with open(server_setting_file_path, 'r') as server_setting_file:
		return load(server_setting_file)

@run_here('..')
def save_setting_file(server_id, server_setting_data):
	server_setting_file_path = f"settings/server/{server_id}.json"
	
	with open(server_setting_file_path, 'w') as server_setting_file:
		dump(server_setting_data, server_setting_file, indent = '\t')

@run_here('..')
def request_server_setting(server_id, *key):
	if server_id == 'default':
		return load_server_setting(server_id)
	
	server_setting_data = load_server_setting(server_id, *key)
	
	if key:
		if len(key) > 1:
			return [server_setting_data[k] for k in key]
		return server_setting_data[key]
	return server_setting_data

@run_here('..')
def overwrite_server_setting(server_id, key = None, value = None, **pairs):
	def update(key, value):
		if k not in server_setting_data:
			raise KeyError(f"Invalid key '{k}'")
		
		server_setting_data[k] = v
	
	server_setting_data = load_server_setting(server_id)
	
	if pairs:
		for k, v in pairs:
			update(k, v)
	elif key and value:
		update(k, v)
	
	save_setting_file(server_id)

@run_here('..')
def update_server_setting(server_id, action = None, pairs = None):
	def add_item():
		value = pairs[key]
		server_setting_data[key] = value
	
	def del_item():
		del server_setting_data[key]
	
	server_setting_data = load_server_setting(server_id)
	actions = {'add': add_item, 'del': del_item}
	
	#action check
	if action and action not in actions:
		raise ValueError(f"invalid action '{action}'")
	
	action = actions[action]
	
	for key in pairs:
		action()
	
	save_setting_file(server_id, server_setting_data)
