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
    return loads(getenv("CONFIG"))


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
