from pathlib import Path
from sys import argv

from click import Path as ClickPath
from click import group, option
from dotenv import load_dotenv

from core.bot import LuxRay
from core.config import Config
from utils.cog import load_cogs

ENV_FILE_PATH = Path(".env")

if ENV_FILE_PATH.exists():
    load_dotenv(ENV_FILE_PATH)


@group()
def main():
    pass


@main.command()
@option(
    "-M",
    "--mode",
    default="dev",
    show_default=True,
    help="Which mode should bot run on",
)
@option(
    "-C",
    "--config-path",
    default="bot-config.toml",
    show_default=True,
    type=ClickPath(dir_okay=False, resolve_path=True),
    help="Path of config file",
)
def run(mode: str = "dev", config_path="bot-config.toml"):
    mode = mode.upper()
    config = Config(config_path, mode)
    bot = LuxRay(config)

    load_cogs(bot, cogs=config.cog_files, cog_folders=config.cog_folders)

    # Create a web servivce
    if mode == "PROD":
        from keep_alive import keep_alive

        keep_alive()
    bot.run(config.bot_token)


if len(argv) == 1:
    run()
else:
    main()
