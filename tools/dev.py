import os
from os import listdir

from .run_here import run_here
from .server_setting import request_server_setting, update_server_setting

__all__ = [
	'sync_server_setting_to_default'
]

@run_here('../settings/server')
def sync_server_setting_to_default():
	default_server_setting = request_server_setting('default')
	default_server_setting_key = set(default_server_setting.keys())
	server_setting_files = listdir('.')
	
	for file in server_setting_files:
		file = file[:-5]
		server_setting = request_server_setting(file)
		server_setting_key = set(server_setting.keys())
		added_key = default_server_setting_key - server_setting_key
		deleted_key = server_setting_key - default_server_setting_key
		
		if added_key:
			added_key = {key: default_server_setting[key] for key in added_key}
			update_server_setting(file, 'add', added_key)
		
		if deleted_key:
			update_server_setting(file, 'del', deleted_key)
