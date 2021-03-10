from json import load
from .run_here import run_here

__all__ = [
	'load_lang'
]

@run_here('..')
def load_lang(server_id = None, *token):
	if server_id == "internal":
		with open("lang/internal.json", 'r', encoding = 'UTF-8') as internal_lang_file:
			lang_file = load(internal_lang_file)
	else:
		try:
			server_id = int(server_id)
			with open(f"settings/server/{server_id}.json", 'r', encoding = 'UTF-8') as server_setting_file:
				with open(f"lang/{load(server_setting_file)['lang']}.json", "r", encoding = "UTF-8") as lang_file:
					lang_file = load(lang_file)
		except ValueError:
			raise ValueError(f"the 'server_id' must be int or 'internal', not {server_id}({server_id.__class__.__name__})")
	
	if not token:
		return lang_file
	
	def get_lang(key):
		if '.' in key:
			lang = lang_file
			
			for k in key.split('.'):
				lang = lang[k]
		else:
			lang = lang_file[key]
		
		return lang
	
	if len(token) == 1:
		return get_lang(token[0])
	return [get_lang(key) for key in token]
