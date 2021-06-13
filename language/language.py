from tools.json_open import json_load
from tools.token import Token, token_get_data
from cog import cog_folder_abbr_to_fullname
from exceptions import LanguageNotSuppot, NoTokenInputError

languages = {
	"en",
	"zh-TW"
}
language_to_name = dict(zip(languages, {
	"English",
	"中文(臺灣)"
}))

language_file_path = "language/{language}.json"
ext_language_file_path = cog_folder_abbr_to_fullname["ext"] + "/{ext_file_name}/language/{language}.json"

class Language:
	def __init__(self, language_file_path: str, language: str):
		if language in languages:
			self.language = language
		else:
			raise LanguageNotSuppot(language)
		
		self.data = json_load(language_file_path.format(language = language))
	
	def load(self):
		return self.data
	
	def request(self, *tokens):
		try:
			return token_get_data(self.data, Token(tokens[0])) if len(tokens) == 1 else [token_get_data(self.data, Token(token)) for token in tokens]
		except IndexError:
			raise NoTokenInputError
