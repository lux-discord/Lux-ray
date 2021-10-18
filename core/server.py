from typing import Union

from disnake.ext.commands import Context
from disnake.message import Message
from exceptions import LanguageNotChange, InvalidPrefix, PrefixNotChange, RoleNotChange
from pymongo.collection import Collection
from utils import Token

from core.prefix import update_prefix

from .db import server_coll
from .language import Language


class ServerBasic():
	def __init__(self, ctx: Context, server_coll: Collection) -> None:
		self.id = ctx.guild.id
		self.ctx = ctx
		self.server_coll = server_coll
	
	def _update_coll(self, update):
		return self.server_coll.update_one({"_id": self.id}, update)
	
	def _update_each(self, properties: dict):
		"""Update attribute data in each place(eg: server_coll, self.data, self.[attr_name], ...)"""
		
		self._update_coll({"$set": properties})
		self._update_attr(properties)
		self.data |= properties
		
		return self.data
	
	def _update_attr(self, update: dict[str]):
		for attr_name, value in update.items():
			if "." in attr_name:
				attr_name, value_token = attr_name.split(".", 1)
				setattr(self, attr_name, Token(value_token).dict_update(getattr(self, attr_name), value))
			else:
				setattr(self, attr_name, value)
	
	def lang_request(self, token: Union[Token, str]) -> Union[str, dict]:
		return self.language.request(token)
	
	def lang_request_many(self, *tokens: Union[Token, str]) -> list[str, dict]:
		return self.language.request_many(*tokens)
	
	async def send_error(self, token: Union[Token, str], **format_kargs) -> Message:
		message = self.lang_request(token).format(**format_kargs)
		return await self.ctx.send(message, delete_after=5)
	
	async def send_warning(self, token: Union[Token, str], **format_kargs) -> Message:
		message = self.lang_request(token).format(**format_kargs)
		return await self.ctx.send(message, delete_after=10)
	
	async def send_info(self, token: Union[Token, str], **format_kargs) -> Message:
		message = self.lang_request(token).format(**format_kargs)
		return await self.ctx.send(message, delete_after=3)

class Server(ServerBasic):
	def __init__(self, ctx: Context) -> None:
		if not isinstance(ctx, Context):
			raise TypeError(f"ctx must be discord.ext.commands.Context, not {ctx.__class__.__name__}")
		
		super().__init__(ctx, server_coll)
		
		if not (server_data := self.server_coll.find_one({"_id": self.id})):
			server_data = {
				"_id": self.id,
				"lang_code": "en",
				"roles": {
					"auto_roles": []
				},
				"able_ext": []
			}
			self.server_coll.insert_one(server_data)
		
		self.data = server_data
		# add shortcut of value in server_data
		self.lang_code: str = server_data["lang_code"]
		self.roles: dict = server_data["roles"]
		self.able_ext: list = server_data["able_ext"]
		# create Language instance and assign
		self.language = Language(self.lang_code)
	
	def update_prefix(self, status, prefix):
		if prefix == self.ctx.prefix:
			raise PrefixNotChange
		
		try:
			update_prefix(self.id, status, prefix)
			# because prefix don't in attrs, server_coll and self.data
			# so don't need use self._update at end
		except InvalidPrefix:
			raise InvalidPrefix(prefix)
	
	def update_lang(self, lang_code):
		if lang_code == self.lang_code:
			raise LanguageNotChange
		
		self._update_attr({"language": Language(lang_code)})
		self._update_each({"lang_code": lang_code})
	
	def update_auto_role(self, role_names):
		if (role_names := sorted(role_names)) != self.roles["auto_roles"]:
			self.roles["auto_roles"] = role_names
		else:
			raise RoleNotChange
		
		self._update_each({"roles.auto_roles": role_names})
