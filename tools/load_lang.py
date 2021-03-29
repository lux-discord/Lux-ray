from json import load

from .run_here import run_here

from exceptions import raise_ssnfe

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
			with open(f"settings/server/{server_id}.json", 'r', encoding = 'UTF-8') as server_setting_file:
				with open(f"lang/{load(server_setting_file)['config']['lang']}.json", "r", encoding = "UTF-8") as lang_file:
					lang_file = load(lang_file)
		except FileNotFoundError:
			raise_ssnfe(server_id)
	
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
