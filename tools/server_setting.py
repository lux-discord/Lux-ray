from json import load, dump

from .run_here import run_here

__all__ = [
	'server_setting'
]

@run_here('..')
def server_setting(server_id, key = None, value = None, action = None):
	def save():
		with open(server_setting_file_path, 'w') as server_setting_file:
			dump(server_setting_data, server_setting_file, indent = '\t')
	
	def update():
		server_setting_data[key] = value
		save()
		
	def delete():
		del server_setting_data[key]
		save()
	
	server_setting_file_path = f"settings/server/{server_id}.json"
	actions = {'add': update, 'del': delete}
	
	with open(server_setting_file_path, 'r') as server_setting_file:
		server_setting_data = load(server_setting_file)
	
	#request all server_setting_data
	if key is None:
		return server_setting_data
	
	#request specified key's value of server_setting_data
	if value is None:
		return server_setting_data[key]
	
	#update specified key's value of server_setting_data
	if action is None and key in server_setting_data:
		update()
		return
	else:
		raise KeyError(f"Invalid key '{key}'")
	
	#add or delete specified key of server_setting_data
	if action not in actions:
		raise ValueError(f"invalid action '{action}'")
	
	actions[action]()
