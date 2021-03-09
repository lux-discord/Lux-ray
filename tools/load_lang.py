from json import load
from .run_here import run_here
import os

__all__ = [
	'load_lang'
]

@run_here('..')
def load_lang(server_id = None):
	if server_id == "internal":
		with open("lang/internal.json", 'r', encoding = 'UTF-8') as internal_lang_file:
			lang_file = load(internal_lang_file)
	elif type(server_id) is int:
		with open(f"settings/server/{server_id}.json", 'r', encoding = "UTF-8") as server_setting:
			with open(f"lang/{load(server_setting)['lang']}.json", 'r', encoding = "UTF-8") as lang_file:
				lang_file = load(lang_file)
	else:
		raise ValueError(f"the 'server_id' must be int or 'internal', not {server_id}({server_id.__class__.__name__})")
	
	return lang_file
