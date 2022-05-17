from pathlib import Path
from sys import argv

from click import Path as ClickPath
from click import group, option
from dotenv import load_dotenv

from core.bot import LuxRay
from core.config import Config

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
def start(mode: str = "dev", config_path="bot-config.toml"):
    mode = mode.upper()
    config = Config(config_path, mode)
    bot = LuxRay(config)
    bot.load_cogs(cog_files=config.cog_files, cog_folders=config.cog_folders)

    if not bot.dev_mode:
        # Create a web service
        from keep_alive import keep_alive

        keep_alive()

    bot.run(config.bot_token)


if len(argv) == 1:
    start()
else:
    main()
