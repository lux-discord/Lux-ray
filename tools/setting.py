from pathlib import Path
from typing import Any, Dict

from cog import cog_folder_abbr_to_fullname
from .json_open import json_load, json_dump
from .run_here import run_here
from .token import Token, token_get_data, token_edit_data

'''
abbr:
	df -> default
	ext -> extension
	stg -> setting
	svr -> server
	
suffix:
	folder -> folder
	file -> file
	path -> folder + file
'''

__all__ = [
	#global variable
	"svr_stg_folder",
	"svr_stg_file",
	"df_svr_stg_file",
	
	"ext_folder",
	"ext_svr_stg_folder",
	
	"svr_stg_path",
	"df_svr_stg_path",
	
	"ext_svr_stg_path",
	"ext_df_svr_stg_path",
	#class
	"Setting",
	"ServerSetting",
	"ExtServerSetting"
]

svr_stg_folder = "../server_setting/"
svr_stg_file = "{svr_id}.json"
df_svr_stg_file = "_default_server_setting.json"

ext_folder = f"../{cog_folder_abbr_to_fullname['ext']}/"
ext_svr_stg_folder = ext_folder + "{ext_file_name}/server_setting/"
#ext class name may not same with file name, and ext's folder use file name, so use "{ext_file_name}" here

svr_stg_path = svr_stg_folder + svr_stg_file
df_svr_stg_path = svr_stg_folder + df_svr_stg_file

ext_svr_stg_path = ext_svr_stg_folder + svr_stg_file
ext_df_svr_stg_path = ext_svr_stg_folder + df_svr_stg_file

class Setting:
	def __init__(self, id):
		self.id = id

class ServerSettingBase:
	def create(self):
		df_svr_stg: dict = json_load(self._default_server_setting_path)
		self.data = df_svr_stg

		json_dump(df_svr_stg, self.path)

		return df_svr_stg
	
	def load(self):
		return self.data if hasattr(self, "data") else self.create()
	
	def request(self, *tokens):
		return token_get_data(self.load(), Token(tokens[0])) if len(tokens) == 1 else [token_get_data(self.load(), Token(token)) for token in tokens]
	
	def edit(self, settings: Dict[str, Any], allow_add_key = False):
		if not hasattr(self, "data"):
			self.create()
		
		for token, value in settings.items():
			self.data = token_edit_data(self.data, Token(token), value, allow_add_key = allow_add_key)
		
		json_dump(self.data, self.path, overwrite = True)

class ServerSetting(Setting, ServerSettingBase):
	def __init__(self, id):
		super().__init__(id)
		self.path = Path(svr_stg_path.format(svr_id = self.id))
		self._default_server_setting_path = Path(df_svr_stg_path)

class ExtServerSetting(Setting, ServerSettingBase):
	def __init__(self, id, ext_file_name):
		"""
		Hint
		----
		ext_file_name is recommended to pass in "__file__" of main ext_file
		"""
		super().__init__(id)
		ext_file_name = Path(ext_file_name).stem
		self.path = Path(ext_svr_stg_path.format(ext_file_name = ext_file_name, svr_id = self.id))
		self._default_server_setting_path = Path(ext_df_svr_stg_path.format(ext_file_name = ext_file_name))
