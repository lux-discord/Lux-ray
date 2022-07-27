from importlib import import_module
from os import getenv
from pathlib import Path
from typing import TYPE_CHECKING

from disnake import Intents
from disnake.utils import search_directory
from tomli import load, loads

from core.database import get_driver
from core.exceptions import InvalidConfigValue

if TYPE_CHECKING:
    from typing import Union


def import_from_path(import_path: str):
    module, name = import_path.rsplit(".", 1)
    return getattr(import_module(module), name)


def load_config_data(config_path: "Union[str, Path]") -> dict:
    if not isinstance(config_path, Path):
        config_path = Path(config_path)

    config_path_exist = config_path.exists()

    print(
        f"Loading config data from '{config_path}'..."
        if config_path_exist
        else "Loading config data from envirment variable..."
    )

    if config_path_exist:
        with open(config_path, "rb") as f:
            return load(f)
    # When the environment variable contains special characters like newlines, tabs...etc
    # getenv will return a string that has been replaced with escape character format (eg: "\\n", "\\t"...)
    # to make it easier for users to read
    # So we need to replace it with the original special character so that tomli can parse it correctly
    config_data = getenv("CONFIG").replace("\\n", "\n").replace("\\t", "\t")
    return loads(config_data)


class Config:
    def __init__(self, config_path: "Union[str, Path]", mode: str) -> None:
        self.__data = load_config_data(config_path)
        self.__mode = mode
        self.__dev_mode = mode == "DEV"

        prefix_data: dict = self.__data["prefix"][self.__mode]
        self.__prefix = self.__get_prefix(prefix_data)
        self.__default_prefix = self.__get_default_prefix(prefix_data)
        self.__cog_files: list[str] = self.__data["cogs"]["file"]
        self.__cog_folders: list[str] = self.__data["cogs"]["folder"]
        self.__all_cog_files = self.__cog_files + [
            file for path in self.__cog_folders for file in search_directory(path)
        ]
        self.__bot_token = self.__get_bot_token()
        self.__test_guilds: list[int] = self.__data["server"]["test_guilds"]
        self.__default_lang_code: str = self.__data["server"]["default_lang_code"]
        self.__owner_ids: list[int] = self.__data["misc"]["owner_ids"]
        self.__color: int = self.__parse_color()
        self.__saucenao_api_key = getenv("SAUCENAO_API_KEY")

    def __get_prefix(self, data: dict) -> "Union[str, list[str], function]":
        type_to_key = {
            "string": "prefix",
            "array": "prefixes",
            "function": "function_path",
        }

        _type = data["type"]

        if not (key := type_to_key.get(_type)):
            config_name = f"prefix.{self.__mode}.type"
            raise InvalidConfigValue(config_name, _type)

        if key == "function_path":
            prefix = import_from_path(data[key])
            config_name = f"prefix.{self.__mode}.function_path"
        else:
            prefix = data[key]
            config_name = f"prefix.{self.__mode}.{key}"

        if not prefix:
            raise InvalidConfigValue(config_name, "None")

        return prefix

    def __get_default_prefix(self, data: dict) -> str:
        return data["prefix"]

    def __get_bot_token(self):
        if token := getenv("TOKEN_ALL"):
            return token

        if token := getenv(f"TOKEN_{self.__mode}"):
            return token

        raise ValueError(f"Environment variable `TOKEN_{self.__mode}` not found")

    def __parse_color(self):
        color: str = self.__data["misc"]["color"]

        if not color.startswith(("#", "0x")):
            raise InvalidConfigValue("misc.color")

        color = color.replace("#", "0x")
        return int(color, 16)

    @property
    def mode(self):
        return self.__mode

    @property
    def dev_mode(self):
        return self.__dev_mode

    @property
    def cog_files(self):
        return self.__cog_files

    @property
    def cog_folders(self):
        return self.__cog_folders

    @property
    def all_cog_files(self):
        return self.__all_cog_files

    @property
    def prefix(self):
        return self.__prefix

    @property
    def default_prefix(self):
        return self.__default_prefix

    @property
    def bot_token(self):
        return self.__bot_token

    @property
    def test_guilds(self):
        return self.__test_guilds

    @property
    def default_lang_code(self):
        return self.__default_lang_code

    @property
    def owner_ids(self):
        return self.__owner_ids

    @property
    def color(self):
        return self.__color

    @property
    def saucenao_api_key(self):
        return self.__saucenao_api_key

    def create_database_client(self):
        print("Creating database client...")
        type_to_path = {"mongodb": "core.database.mongodb.MongoDB"}

        if not (_type := getenv(f"DB_TYPE_{self.__mode}")):
            raise ValueError(f"Environment variable `DB_TYPE_{self.__mode}` not found")

        if _type not in type_to_path:
            raise ValueError(f"Invalid database type `{_type}`")

        if not (host := getenv(f"DB_HOST_{self.__mode}")):
            raise ValueError(f"Environment variable `DB_HOST_{self.__mode}` not found")

        # Maybe add a warning when port is not found?
        port = int(port) if (port := getenv(f"DB_PORT_{self.__mode}")) else None
        driver = get_driver(_type)
        return driver(host=host, port=port)

    def create_intents(self):
        print("Creating intents instance...")
        data = self.__data["intent"]
        base = data["base"]
        items = data["items"]

        try:
            base_intent: Intents = getattr(Intents, base)()
        except AttributeError:
            raise InvalidConfigValue("intent.base", base)

        try:
            for name, value in items.items():
                setattr(base_intent, name, value)
        except AttributeError as e:
            # e.args[0] -> error message
            # split("'")[-2] -> get attribute name that not exists
            item_value = e.args[0].split("'")[-2]
            raise InvalidConfigValue("intent.item", item_value)

        return base_intent
