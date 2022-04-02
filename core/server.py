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
	
	def request_message(self, token: Token):
		"""
		Argument
		--------
		token: utils.token.Token
			token that use to request message
		
		Return
		------
		The message that request
		
		Return type
		-----------
		str
		"""
		language = GeneralLanguage(self.lang_code)
		return language.request_message(token)
	
	async def _send(self, ctx, message: Union[str, Token], *, delete_after=None, **_format):
		if isinstance(message, Token):
			message = self.request_message(message)
		
		if _format:
			message = message.format(**_format)
		
		return ctx.send(message, delete_after=delete_after)
	
	async def send_info(self, ctx, message: Union[str, Token], **_format):
		return await self._send(ctx, message, delete_after=2, **_format)
	
	async def send_warning(self, ctx, message: Union[str, Token], **_format):
		return await self._send(ctx, message, delete_after=6, **_format)
	
	async def send_error(self, ctx, message: Union[str, Token], **_format):
		return await self._send(ctx, message, delete_after=10, **_format)
	