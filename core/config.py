from os import getenv
from pathlib import Path
from typing import TYPE_CHECKING

from disnake import Intents
from tomli import load, loads

from exceptions import ConfigInvalid
from utils.misc import import_from_path

if TYPE_CHECKING:
    from typing import Union


def load_config_data(config_path) -> dict:
    if Path(config_path).exists():
        with open(config_path, "rb") as f:
            return load(f)
    # When the environment variable contains special characters like newlines, tabs...etc
    # getenv will return a string that has been replaced with escape character format (eg: "\\n", "\\t"...)
    # to make it easier for users to read
    # So we need to replace it with the original special character so that tomli can parse it correctly
    config_data = getenv("CONFIG").replace("\\n", "\n").replace("\\t", "\t")
    return loads(config_data)


class Config:
    def __init__(self, config_path, mode) -> None:
        self.__data = load_config_data(config_path)
        self.__mode = mode

        prefix_data = self.__data["prefix"][self.__mode]
        self.__prefix = self.__get_prefix(prefix_data)
        self.__default_prefix = self.__get_default_prefix(prefix_data)
        self.__cog_files = self.__data["cogs"]["file"]
        self.__cog_folders = self.__data["cogs"]["folder"]
        self.__bot_token = self.__get_bot_token()
        self.__default_lang_code = self.__data["server"]["default_lang_code"]
        self.__owner_ids = self.__data["misc"]["owner_ids"]

    def __get_prefix(self, data) -> "Union[str, list[str], function]":
        type_to_key = {
            "string": "prefix",
            "array": "prefixes",
            "function": "function_path",
        }

        _type = data["type"]

        if not (key := type_to_key.get(_type)):
            config_name = f"prefix.{self.__mode}.type"
            raise ConfigInvalid(config_name, _type)

        if key == "function_path":
            prefix = import_from_path(data[key])
            config_name = f"prefix.{self.__mode}.function_path"
        else:
            prefix = data[key]
            config_name = f"prefix.{self.__mode}.{key}"

        if not prefix:
            raise ConfigInvalid(config_name, "None")

        return prefix

    def __get_default_prefix(self, data) -> str:
        return data["prefix"]

    def __get_bot_token(self):
        if token := getenv("TOKEN_ALL"):
            return token

        if token := getenv(f"TOKEN_{self.__mode}"):
            return token

        raise ValueError(f"Environment variable `TOKEN_{self.__mode}` not found")

    @property
    def mode(self):
        return self.__mode

    @property
    def cog_files(self):
        return self.__cog_files

    @property
    def cog_folders(self):
        return self.__cog_folders

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
    def default_lang_code(self):
        return self.__default_lang_code

    @property
    def owner_ids(self):
        return self.__owner_ids

    def get_database_client(self):
        type_to_path = {"mongodb": "core.database.mongodb.MongoDB"}

        if not (_type := getenv(f"DB_TYPE_{self.__mode}")):
            raise ValueError(f"Environment variable `DB_TYPE_{self.__mode}` not found")

        if _type not in type_to_path:
            raise ValueError(f"Invalid database type `{_type}`")

        if not (host := getenv(f"DB_HOST_{self.__mode}")):
            raise ValueError(f"Environment variable `DB_HOST_{self.__mode}` not found")

        # Maybe add a warning when port is not found?
        port = int(port) if (port := getenv(f"DB_PORT_{self.__mode}")) else None
        _class = import_from_path(type_to_path[_type])
        return _class(host=host, port=port)

    def get_intents(self):
        data = self.__data["intent"]
        base = data["base"]
        items = data["items"]

        try:
            base_intent = getattr(Intents, base)()
        except AttributeError:
            raise ConfigInvalid("intent.base", base)

        try:
            for name, value in items.items():
                setattr(base_intent, name, value)
        except AttributeError as e:
            # e.args[0] -> error message
            # split("'")[-2] -> get attribute name that not exists
            item_value = e.args[0].split("'")[-2]
            raise ConfigInvalid("intent.item", item_value)

        return base_intent
