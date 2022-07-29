from pathlib import Path
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from fire import Fire

from core.bot import LuxRay

if TYPE_CHECKING:
    from typing import Union


class Main:
    """The main program of Lux-ray

    If flag `--mode` IS NOT provided, it defaults to "DEV"
    If flag `--config_path` IS NOT provided, it default to "bot-config-dev.toml"(in "DEV" mode) or "bot-config.toml"(in "PROD" mode) in the bot root directory
    If flag `--env_file_path` IS provided, bot will read config data from the env file if the config file is not exists
    """

    def __init__(
        self,
        mode: str = None,
        config_path: "Union[str, Path]" = None,
        env_file_path: "Union[str, Path]" = None,
    ) -> None:
        # `mode` type check
        if not mode:
            mode = "DEV"
        elif not isinstance(mode, str):
            err_msg = f"argument `mode` expected str or NoneType, not {mode.__class__.__name__}"
            raise TypeError(err_msg)
        # `mode` value check
        if (mode := mode.upper()) not in {"DEV", "PROD"}:
            raise ValueError(
                "if argument `mode` is provided, it must be 'DEV' or 'PROD'(case insensitive)"
            )

        # `config_path` type check
        if not config_path:
            config_path = (
                Path("bot-config-dev.toml")
                if mode == "DEV"
                else Path("bot-config.toml")
            )
        elif not isinstance(config_path, Path):
            try:
                config_path = Path(config_path)
            except TypeError:
                err_msg = f"argument `config_path` expected str, pathlib.Path or NoneType, not {config_path.__class__.__name__}"
                raise TypeError(err_msg)

        # Load env file if provided and exists
        if env_file_path:
            # `env_file_path` type check
            if not isinstance(env_file_path, Path):
                try:
                    env_file_path = Path(env_file_path)
                except TypeError:
                    err_msg = f"argument `env_file_path` expected str, pathlib.Path or NoneType, not {env_file_path.__class__.__name__}"
                    raise TypeError(err_msg)
            # `env_file_path` exists check
            if not env_file_path.exists():
                err_msg = f"env file `{env_file_path}` not found"
                raise FileNotFoundError(err_msg)

            load_dotenv(env_file_path)

        self.mode = mode
        self.is_dev = mode == "DEV"
        self.config_path = config_path

    def run(self, **options) -> None:
        """Start running Lux-ray"""
        """Start running Lux-ray

        See https://docs.disnake.dev/en/stable/api.html#disnake.Client for all avaliable flags(parameters)

        Flags
        -----
        `--reconnect`: See https://docs.disnake.dev/en/stable/api.html?highlight=connect#disnake.Client.connect for more infomation
        """
        bot = LuxRay(self.config_path, self.mode, **options)
        bot.init()
        bot.run()


if __name__ == "__main__":
    Fire(Main)
