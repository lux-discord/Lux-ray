from .json_open import json_load
from .run_here import run_here
from .setting import request_server_setting
from .token import Token, get_data_with_token

__all__ = [
	"load_internal",
	"load_lang"
]

@run_here
def load_internal():
	return json_load("../internal.json")

@run_here("..")
def load_lang(server_ID, *tokens: str):
	server_lang = request_server_setting(server_ID, "config.language")
	lang_data = json_load(f"language/{server_lang}.json")
	
	if not tokens:
		return lang_data
	
	return get_data_with_token(lang_data, Token(tokens[0])) if len(tokens) == 1 else [get_data_with_token(lang_data, Token(token)) for token in tokens]
