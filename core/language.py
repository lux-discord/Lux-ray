from typing import Union

from exceptions import LanguageNotSupport
from tool.json_file import load_file
from tool.token import Token

SUPPORT_LANGUAGE = {
	"en": "English",
	"zh-TW": "中文(臺灣)"
}
LANG_FILE_PATH = "language/{lang_code}.json"

class Language():
	def __init__(self, lang_code: str, support_lang: dict=SUPPORT_LANGUAGE, lang_file_path: str=LANG_FILE_PATH) -> None:
		"""
		Parameter
		---------
		lang_code: `str`
			The language code you want to use
		support_lang: `dict`
			All supported languages and their names
			
			format: `{language_code: language_name}`
		lang_file_path: `str`
			Paht to language file
			
			default: `language/{lang_code}.json`
		"""
		if lang_code in support_lang:
			self.code = lang_code
			self.name = support_lang[lang_code]
		else:
			raise LanguageNotSupport(lang_code)
    
		self.data = load_file(lang_file_path.format(lang_code=lang_code))
	
	def request(self, token: Union[Token, str], *, delimiter: str=None) -> Union[str, dict]:
		try:
			return token.get(self.data)
		except AttributeError:
			return Token(token, delimiter).get(self.data) if delimiter else Token(token).get(self.data)
	
	def request_many(self, *tokens: Union[Token, str]) -> list[str, dict]:
		return [self.request(token) for token in tokens]
	
	def __str__(self):
		return self.code
	
	def __repr__(self) -> str:
		return f"<Language_code: {self.code}, Name: {self.name}>"
	
	def __eq__(self, o: object) -> bool:
		return self.code == str(o)

def generate_lang_file_path(lang_folder_path: str):
	return lang_folder_path + "{lang_code}.json" if lang_folder_path.endswith("/") else lang_folder_path + "/{lang_code}.json"
