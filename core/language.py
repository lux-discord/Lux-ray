from pathlib import Path

from exceptions import LanguageNotSupport, ItemNotExists
from utils.json_file import load_file
from utils.token import Token

GLOBAL_LANGUAGE_DIR = Path("language")
GLOBAL_SUPPORT_LANGUAGE = {lang_file.stem for lang_file in GLOBAL_LANGUAGE_DIR.iterdir()}

# For custom language file
def get_support_language(lang_dir: Path):
	return {lang_file.name for lang_file in lang_dir.iterdir()}

def language_support_check(lang_dir: Path, lang_code: str):
	return lang_code in get_support_language(lang_dir)

class LanguageBase():
	def __init__(self) -> None:
		self.data = {}
		
		raise NotImplementedError
	
	def request_message(self, token: Token) -> str:
		if message := token.dict_get(self.data):
			return message
		raise ItemNotExists(token)
	
	def bulk_request_message(self, *tokens: Token):
		return [self.request_message(token) for token in tokens]

class GeneralLanguage(LanguageBase):
	def __init__(self, lang_code: str) -> None:
		if lang_code not in GLOBAL_SUPPORT_LANGUAGE:
			raise LanguageNotSupport(lang_code)
		
		self.data = load_file(GLOBAL_LANGUAGE_DIR/(lang_code+".json"))
