from typing import Union

from core.data import ServerData
from core.language import GeneralLanguage
from utils.token import Token


class Server():
	def __init__(self, server_data: ServerData) -> None:
		self.items = server_data.items
		self.id = server_data.id
		self.lang_code = server_data.lang_code
		self.role = server_data.role
	
	def update(self, **update):
		"""
		Generatr a ServerData with self.items and gived update
		
		Return
		------
		A ServerData instance base on self.items and update
		
		Return type
		-----------
		`core.data.ServerData`
		"""
		return ServerData.from_items(self.items | update)
	
	def translate(self, message):
		"""
		Argument
		--------
		message: str
			message that need translate
		
		Return
		------
		The message that translated
		
		Return type
		-----------
		str
		"""
		language = GeneralLanguage(self.lang_code)
		return language.request_message(message)
	
	async def _send(self, ctx, message: str, *, delete_after=None, **_format):
		if self.lang_code != GLOBAL_DEFAULT_LANGUAGE:
			message = self.translate(message)
		
		if _format:
			message = message.format(**_format)
		
		return await ctx.send(message, delete_after=delete_after)
	
	async def send_info(self, ctx, message: str, **_format):
		return await self._send(ctx, message, delete_after=2, **_format)
	
	async def send_warning(self, ctx, message: str, **_format):
		return await self._send(ctx, message, delete_after=6, **_format)
	
	async def send_error(self, ctx, message: str, **_format):
		return await self._send(ctx, message, delete_after=10, **_format)
