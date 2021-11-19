from functools import cache
from pathlib import Path
from typing import Union

from exceptions import LanguageNotSupport, MessageNotExists
from utils.json_file import load_file
from utils.token import Token

@cache
def get_support_language(lang_dir: Path):
	return {lang_file.name for lang_file in lang_dir.iterdir()}

@cache
def request_message(lang_dir: Path, lang_code: str, token: Token):
	return request_lang(lang_dir, lang_code).request_message(token)

@cache
def request_lang(lang_dir: Path, lang_code: str):
	return LanguageBase(lang_dir, lang_code)

class LanguageBase():
	def __init__(self, lang_dir: Path, lang_code: str) -> None:
		if lang_code not in get_support_language(lang_dir):
			raise LanguageNotSupport(lang_code)
		
		self.data = load_file(lang_dir/lang_code+".json")
	
	def request_message(self, token: Token) -> str:
		if message := token.dict_get(self.data):
			return message
		raise MessageNotExists(token)
	
	def bulk_request_message(self, *tokens: Token):
		return [self.request_message(token) for token in tokens]

class Language(LanguageBase):
	def __init__(self, lang_code: str) -> None:
		"""
		Parameter
		---------
		lang_code: `str`
			The language code you want to use
		"""
		super().__init__(Path("language"), lang_code)
	
	def request_message(self, token: Union[str, Token]):
		return super().request_message(token if isinstance(token, Token) else Token(token))
	
	@cache
	def bulk_request_message(self, *tokens: Union[str, Token]):
		return super().bulk_request_message(*tokens)
