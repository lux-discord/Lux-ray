from json import load, dump

from .run_here import run_here

@run_here('..')
def server_setting(server_id, key = None, value = None):
	server_setting_file_path = f"settings/server/{server_id}.json"
	with open(server_setting_file_path, 'r') as server_setting_file:
		server_setting_data = load(server_setting_file)
	
	if key is None:
		return server_setting_data
	if key is not None:
		if value is None:
			return server_setting_data[key]
		
		server_setting_data[key] = value
		with open(server_setting_file_path, 'w') as server_setting_file:
			dump(server_setting_data, server_setting_file, indent = '\t')
