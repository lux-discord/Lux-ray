from pathlib import Path

from tomli import load

GLOBAL_LOCALES_DIR = Path("locales")
GLOBAL_SUPPORT_LANGUAGE = {
    locale_file.stem for locale_file in GLOBAL_LOCALES_DIR.iterdir()
}
GLOBAL_DEFAULT_LANGUAGE = "en"

global_language_cache: dict[str] = {}


class LanguageBase:
    def __init__(
        self, lang_code: str, *, support_language: set, locale_dir: Path
    ) -> None:
        if lang_code not in support_language:
            raise ValueError(f"Language '{lang_code}' is not supported")

        self.lang_code = lang_code

        with open(locale_dir / (lang_code + ".toml"), "rb") as f:
            self.data: dict[str, str] = load(f)

    def request_message(self, token: str) -> str:
        return self.data[token]

    def bulk_request_message(self, *tokens: str):
        return [self.request_message(token) for token in tokens]


class GeneralLanguage(LanguageBase):
    def __init__(self, lang_code: str) -> None:
        super().__init__(
            lang_code,
            support_language=GLOBAL_SUPPORT_LANGUAGE,
            locale_dir=GLOBAL_LOCALES_DIR,
        )


# For GeneralLanugage
def get_language(lang_code: str) -> GeneralLanguage:
    if lang_code not in global_language_cache:
        global_language_cache[lang_code] = GeneralLanguage(lang_code)
    return global_language_cache[lang_code]


# `get_language` function for other subclass of LanguageBase is in plan


# For custom locale file
def get_support_language(locale_dir: Path):
    return {locale_file.stem for locale_file in locale_dir.iterdir()}


def language_support_check(locale_dir: Path, lang_code: str):
    return lang_code in get_support_language(locale_dir)
