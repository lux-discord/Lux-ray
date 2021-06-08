from typing import Any, Dict
from .json_open import json_load, json_dump
from .run_here import run_here
from .token import Token, get_data_with_token, edit_data_with_token

__all__ = [
	"create_server_setting",
	"load_default_server_setting",
	"load_server_setting",
	"request_server_setting",
	"edit_server_setting"
]

#global variable
default_server_setting_file_path = "../server_setting/_default_server_setting.json"

#global function
def format_server_setting_file_path(server_id):
	return f"../server_setting/{server_id}.json"

#server setting
@run_here
def create_server_setting(server_id) -> dict:
	default_server_setting = load_default_server_setting()
	
	json_dump(default_server_setting, format_server_setting_file_path(server_id))
	
	return default_server_setting

@run_here
def load_default_server_setting() -> dict:
	return json_load(default_server_setting_file_path)

@run_here
def load_server_setting(server_id) -> dict:
	"""
	Return ALL the server setting data with gived server_id
	"""
	try:
		return json_load(format_server_setting_file_path(server_id))
	except FileNotFoundError:
		return create_server_setting(server_id)

@run_here
def request_server_setting(server_id, *tokens: str):
	server_setting_data: dict = load_server_setting(server_id)
	
	return get_data_with_token(server_setting_data, Token(tokens[0])) if len(tokens) == 1 else [get_data_with_token(server_setting_data, Token(token)) for token in tokens]

@run_here
def edit_server_setting(server_id, settings: Dict[str, Any]):
	server_setting = load_server_setting(server_id)
	
	for token, value in settings.items():
		server_setting = edit_data_with_token(server_setting, Token(token), value)
	
	json_dump(server_setting, format_server_setting_file_path(server_id))
