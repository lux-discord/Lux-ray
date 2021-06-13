from pathlib import Path
from typing import Any, Dict

from language.language import Language, language_file_path, ext_language_file_path

from .json_open import json_load, json_dump
from .token import Token, token_get_data, token_edit_data

from cog import cog_folder_abbr_to_fullname
from exceptions import NoTokenInputError

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

svr_stg_folder = "server_setting/"
svr_stg_file = "{svr_id}.json"
df_svr_stg_file = "_default_server_setting.json"

ext_folder = f"{cog_folder_abbr_to_fullname['ext']}/"
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
	def __init__(self):
		self.path = Path(".")
	
	def create(self):
		"""Create server setting file and save it to self.path
		
		Return
		------
		default server setting data
		"""
		df_svr_stg: dict = json_load(self.default_server_setting_path)
		self.data = df_svr_stg

		json_dump(df_svr_stg, self.path)

		return df_svr_stg
	
	def load(self):
		"""Load self.data, if no self.data, create and return it
		
		Return
		------
		self.data if created, else default server setting data
		"""
		try:
			return self.data
		except AttributeError:
			if self.path.exists():
				self.data = json_load(self.path)
				
				return self.data
			else:
				return self.create()
	
	def request(self, *tokens):
		"""Request specified data in self.data with token(s)
		
		Parameter
		---------
		tokens: `Token`
			token(s) that use to request data, must be Token type
		
		Raise
		-----
		KeyError
			if key in token not in self.data
		NoTokenInputError
			if no token input
		
		Return
		------
		data that token(s) request, if has multiple token, data will be list type
		"""
		data = self.load()
		
		try:
			return token_get_data(data, tokens[0]) if len(tokens) == 1 else [token_get_data(data, token) for token in tokens]
		except KeyError:
			raise KeyError
		except IndexError:
			raise NoTokenInputError
	
	def edit(self, settings: Dict[Token, Any], *, allow_add_key = False):
		"""Edit self.data with dict of Token and value
		
		Parameter
		---------
		allow_add_key: `bool`
			if True, add key when token in settings not in self.data else raise KeyError
		
		Raise
		-----
		KeyError
			if token in settings not in self.data and not allow_add_key
		
		Return
		------
		self.data after edit
		"""
		if not hasattr(self, "data"):
			self.create()
		
		try:
			for token, value in settings.items():
				self.data = token_edit_data(self.data, token, value, allow_add_key = allow_add_key)
		except KeyError:
			raise KeyError
		
		json_dump(self.data, self.path, overwrite = True)
		return self.data
	
	def delete(self, *, force = False):
		"""Delete server setting file
		
		Parameter
		---------
		force: `bool`
			if True, ignore FileNotFoundError
		
		Raise
		-----
		FileNotFoundError
			if file already deleted and not force
		"""
		try:
			self.path.unlink(force)
		except FileNotFoundError:
			raise FileNotFoundError
	
	def load_lang(self):
		try:
			return self.language.load()
		except AttributeError:
			return self.init_lang().load()
	
	def request_lang(self, *tokens):
		"""Request specified language data in self.language with token(s)
		"""
		try:
			return self.language.request(*tokens)
		except AttributeError:
			return self.init_lang().request(*tokens)

class ServerSetting(Setting, ServerSettingBase):
	def __init__(self, id):
		super().__init__(id)
		self.path = Path(svr_stg_path.format(svr_id = self.id))
		self.default_server_setting_path = Path(df_svr_stg_path)
	
	def to_ext(self, ext_file_name):
		return ExtServerSetting(self.id, ext_file_name)
	
	def init_lang(self):
		self.language = Language(language_file_path, self.request(Token("config.language")))

class ExtServerSetting(Setting, ServerSettingBase):
	def __init__(self, id, file_name):
		super().__init__(id)
		self.file_name = Path(file_name).stem
		self.path = Path(ext_svr_stg_path.format(ext_file_name = self.file_name, svr_id = self.id))
		self.default_server_setting_path = Path(ext_df_svr_stg_path.format(ext_file_name = self.file_name))
	
	def to_main(self):
		return ServerSetting(self.id)
	
	def init_lang(self):
		self.language = Language(ext_language_file_path.format(ext_file_name = self.file_name, language = "{language}"), self.to_main().request(Token("config.language")))
		
		return self.language
