from os import getenv
from pathlib import Path

from disnake import Intents
from disnake.utils import search_directory
from tomli import load, loads

from core.database import get_driver


class Config:
    with open("sample-bot-config.toml", "rb") as f:
        DEFAULT_CONFIG: dict[str, dict] = load(f)

    def __init__(self, config_path: Path, mode: str) -> None:
        self.__path = config_path
        self.__data = self.__load_data()
        self.__mode = mode
        self.__is_dev = mode == "DEV"

        self.__cog_files: list[str] = self.__data["cog"]["files"]
        self.__cog_folders: list[str] = self.__data["cog"]["folders"]
        self.__all_cog_files = self.__cog_files + [
            file for path in self.__cog_folders for file in search_directory(path)
        ]
        self.__intents = self.__generate_intents()
        self.__default_lang_code: str = self.__data.get(
            "server", self.DEFAULT_CONFIG["server"]
        ).get("default_lang_code", "en")
        self.__owner_ids: list[int] = self.__data.get(
            "misc", self.DEFAULT_CONFIG["misc"]
        ).get("owner_ids", [])
        self.__color: int = self.__parse_color()
        self.__test_guilds: list[int] = self.__data.get(
            "dev", self.DEFAULT_CONFIG["dev"]
        ).get("test_guilds", [])

        self.__saucenao_api_key = getenv("SAUCENAO_API_KEY")

    def __load_data(self):
        if self.__path.exists():
            print(f"Loading config data from '{self.__path}'...")

            with open(self.__path, "rb") as f:
                data: dict[str, dict] = load(f)
        else:
            print(
                f"Config path '{self.__path}' not exists, use default config data from 'sample-bot-config.toml'"
            )

            data = self.DEFAULT_CONFIG

        print("Loading config data from envirment variable...")

        if data := getenv("CONFIG").replace("\\n", "\n").replace("\\t", "\t"):
            return loads(data)
        raise ValueError(f"Environment variable `CONFIG` not found")

    def __generate_intents(self):
        data: dict = self.__data.get("intents", self.DEFAULT_CONFIG["intents"])
        base: str = data.get("base", "default").lower()
        flags: dict = data.get("flags", {})

        if base not in {"all", "default", "none"}:
            raise ValueError(
                "config item `intents.base` must be 'all', 'default' or 'none'(case insensitive)"
            )

        base_intent: Intents = getattr(Intents, base)()

        try:
            for name, value in flags.items():
                setattr(base_intent, name, value)
        except AttributeError as e:
            err_msg: str = e.args[0]
            flag_name = err_msg.split("'")[-2]
            raise ValueError(f"`{flag_name}` is not a valid flag for intents")

        return base_intent

    def __parse_color(self):
        color = self.__data.get("misc", self.DEFAULT_CONFIG["misc"]).get(
            "color", "0x66E8E4"
        )

        if not color.startswith(("#", "0x")):
            raise ValueError("config item `misc.color` must starts with '#' or '0x'")

        color = color.replace("#", "0x")
        return int(color, 16)

    @property
    def path(self):
        return self.__path

    @property
    def data(self):
        return self.__data

    @property
    def mode(self):
        return self.__mode

    @property
    def is_dev(self):
        return self.__is_dev

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
    def intents(self):
        return self.__intents

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
    def test_guilds(self):
        return self.__test_guilds

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

    def get_bot_token(self):
        if token := getenv("TOKEN_ALL"):
            return token

        if token := getenv(f"TOKEN_{self.__mode}"):
            return token

        raise ValueError(f"Environment variable `TOKEN_{self.__mode}` not found")
