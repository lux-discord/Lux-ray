from json import load

from .run_here import run_here

@run_here('..')
def server_setting(server_id):
	with open(f"settings/server/{server_id}.json") as server_setting_file:
		return load(server_setting_file)