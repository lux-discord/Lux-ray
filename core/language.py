from pathlib import Path

from exceptions import LanguageNotSupport
from utils.toml_file import load_file

GLOBAL_LOCALES_DIR = Path("locales")
GLOBAL_SUPPORT_LANGUAGE = {locale_file.stem for locale_file in GLOBAL_LOCALES_DIR.iterdir()}
GLOBAL_DEFAULT_LANGUAGE = "en"

# For custom locale file
def get_support_language(locale_dir: Path):
	return {locale_file.stem for locale_file in locale_dir.iterdir()}

def language_support_check(locale_dir: Path, lang_code: str):
	return lang_code in get_support_language(locale_dir)

class LanguageBase():
	def __init__(self, lang_code, *, support_language: set, locale_dir: Path) -> None:
		if lang_code not in support_language:
			raise LanguageNotSupport(lang_code)
		
		self.lang_code = lang_code
		self.data = load_file(locale_dir/(lang_code+".toml"))
	
	def request_message(self, token: str) -> str:
		return self.data[token]
	
	def bulk_request_message(self, *tokens: str):
		return [self.request_message(token) for token in tokens]

class GeneralLanguage(LanguageBase):
	def __init__(self, lang_code: str) -> None:
		super().__init__(lang_code, support_language=GLOBAL_SUPPORT_LANGUAGE, locale_dir=GLOBAL_LOCALES_DIR)
