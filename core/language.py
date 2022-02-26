from pathlib import Path
from typing import Union

from exceptions import LanguageNotSupport, MessageNotExists
from utils.json_file import load_file
from utils.token import Token

GLOBAL_LANGUAGE_DIR = Path("language")

def get_support_language(lang_dir: Path):
	return {lang_file.name for lang_file in lang_dir.iterdir()}

def language_support_check(lang_dir: Path, lang_code: str):
	return lang_code in get_support_language(lang_dir)

class LanguageBase():
	def __init__(self, lang_dir: Path, lang_code: str) -> None:
		if not language_support_check(lang_dir, lang_code):
			raise LanguageNotSupport(lang_code)
		
		self.data = load_file(lang_dir/lang_code+".json")
	
	def request_message(self, token: Union[str, Token]) -> str:
		token = token if isinstance(token, Token) else Token(token)
		
		if message := token.dict_get(self.data):
			return message
		raise MessageNotExists(token)
	
	def bulk_request_message(self, *tokens: Union[str, Token]):
		return [self.request_message(token) for token in tokens]

class Language(LanguageBase):
	def __init__(self, lang_code: str) -> None:
		"""
		Parameter
		---------
		lang_code: `str`
			The language code you want to use
		"""
		super().__init__(PUBLIC_LANGUAGE_DIR, lang_code)
