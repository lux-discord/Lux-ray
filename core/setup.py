from os import getenv
from pathlib import Path

from tomli import load, loads

from core.bot import LuxRay
from core.config import get_prefix, intent_generater
from utils.json_file import load_file


def get_loading_message() -> list:
    return load_file("loading_message.json")


def get_bot_config(config_path) -> dict:
    if Path(config_path).exists():
        with open(config_path, "rb") as f:
            return load(f)
    # When the environment variable contains special characters like newlines, tabs...etc
    # getenv will return a string that has been replaced with escape character format (eg: "\\n", "\\t"...)
    # to make it easier for users to read
    # So we need to replace it with the original special character so that tomli can parse it correctly
    config_data = getenv("CONFIG").replace("\\n", "\n").replace("\\t", "\t")
    return loads(config_data)


def setup_bot(config, mode):
    # Create Bot instance
    bot = LuxRay(
        command_prefix=get_prefix(config, mode),
        owner_ids=config["misc"]["owner_ids"],
        intents=intent_generater(config, mode),
        config=config,
        mode=mode,
    )

    return bot
