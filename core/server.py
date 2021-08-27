from typing import Union

from discord.ext.commands import Context
from exceptions import LanguageNotChange, PrefixInvalid, RoleNotChange
from pymongo.collection import Collection
from tool.token import Token

from core.prefix import update_prefix as _update_prefix

from .db import bot_db
from .language import Language

server_coll = bot_db["server"]

class ServerBasic():
	def __init__(self, server_coll: Collection) -> None:
		self.server_coll = server_coll
	
	def _server_coll_update_one(self, update):
		return self.server_coll.update_one({"server_id": self.id}, update)
	
	def _update(self, properties: dict):
		self._server_coll_update_one({"$set": properties})
		self.data |= properties
		return self.data
	
	def lang_request(self, token: Union[Token, str]) -> Union[str, dict]:
		return self.language.request(token)
	
	def lang_request_many(self, *tokens: Union[Token, str]) -> list[str, dict]:
		return self.language.request_many(*tokens)
	
	def update_lang(self, lang_code):
		if lang_code == self.lang_code:
			raise LanguageNotChange
		
		self.language = Language(lang_code)
		self.lang_code = lang_code
		self._update({"lang_code":lang_code})

class Server(ServerBasic):
	def __init__(self, ctx: Context) -> None:
		super().__init__(server_coll)
		
		if not isinstance(ctx, Context):
			raise TypeError(f"ctx must be discord.ext.commands.Context, not {ctx.__class__.__name__}")
		
		id = ctx.guild.id
		
		if not (server_data := self.server_coll.find_one({"server_id": id})):
			server_data = {
				"server_id": id,
				"lang_code": "en",
				"roles": {
					"auto_roles": []
				},
				"able_ext": []
			}
			self.server_coll.insert_one(server_data)
		
		self.id = id
		self.data = server_data
		self.lang_code = server_data["lang_code"]
		self.roles = server_data["roles"]
		self.able_ext = server_data["able_ext"]
		self.language = Language(self.lang_code)
	
	def _update(self, properties: dict):
		self.data |= properties
		server_coll.update_one({"server_id": self.id}, properties)
		print(properties)
	
	def lang_request(self, token: Union[Token, str]) -> Union[str, dict]:
		return self.language.request(token)
	
	def lang_request_many(self, *tokens: Union[Token, str]) -> list[str, dict]:
		return self.language.request_many(*tokens)
	
	def update_lang(self, lang_code):
		if lang_code == self.lang_code:
			raise LanguageNotChange
		
		self.language = Language(lang_code)
		self.lang_code = lang_code
		self._update({"lang_code": lang_code})
	
	def update_prefix(self, status, prefix):
		try:
			_update_prefix(self.id, status, prefix)
		except PrefixInvalid:
			raise PrefixInvalid(prefix)
	
	def update_auto_role(self, *roles_id):
		if roles_id := list(roles_id) != self.roles:
			self.roles = roles_id
		else:
			raise RoleNotChange
		
		self._update({"roles": {"auto_role": self.roles}})
