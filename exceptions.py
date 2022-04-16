class LRBError(Exception):
    """
    Base exception of Lux-ray bot
    """

    pass


# Check Failure
class CheckFailure(LRBError):
    pass


class MissingPermissions(CheckFailure):
    def __init__(self, missing_permissions: list[str]) -> None:
        self.missing_permissions: list[str] = missing_permissions

        missing = [
            perm.replace("_", " ").replace("guild", "server").title()
            for perm in self.missing_permissions
        ]

        self.massage = ", ".join(missing)

    def __str__(self) -> str:
        return f"Missing permission(s): {self.massage}"


# Invalid user input exceptions
class InvalidUserInput(LRBError):
    """
    Base exception of all invalid user input
    """

    pass


class LanguageNotSupport(InvalidUserInput):
    """
    Raise when language is not support
    """

    def __init__(self, lang_code) -> None:
        self.lang_code = lang_code

    def __str__(self):
        return f"language(code) '{self.lang_code}' not suppot"


class InvalidMessageLink(InvalidUserInput):
    def __init__(self, msg_link) -> None:
        self.msg_link = msg_link

    def __str__(self) -> str:
        return f"Invalid message link '{self.msg_link}'"


class InvalidChannelID(InvalidUserInput):
    def __init__(self, ch_id):
        self.ch_id = ch_id

    def __str__(self):
        return f"Invalid channel ID '{self.ch_id}'"


class InvalidMessageID(InvalidUserInput):
    def __init__(self, msg_id) -> None:
        self.msg_id = msg_id

    def __str__(self):
        return f"Invalid message ID '{self.msg_id}'"


# Internal exceptions
class InternalError(LRBError):
    pass


class InvalidToken(InternalError):
    def __init__(self, *args: object, **kargs) -> None:
        super().__init__(*args)
        self.kargs = kargs

    def __str__(self) -> str:
        file_name = __file__.split("\\")[-1][:-2]
        self_name = self.__class__.__name__
        token_str = self.kargs.get("token", self.kargs.get("token_str"))
        invalid_key = self.kargs.get("key")
        delimiter = self.kargs.get("delimiter")

        if not token_str:
            raise ValueError("No token(str) input")

        if not invalid_key:
            raise ValueError("No invalid key input")

        if not delimiter:
            raise ValueError("No delimiter input")

        return f"{token_str}\n{' '*(len(file_name)+len(self_name)+3+len(delimiter))}{'^'*len(invalid_key)}"
        # why +3 when repeating " ":
        # 1 for '.' betwean file name and self name
        # 2 for ': ' after self name


class ItemNotExists(InternalError):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return f"Item of token '{self.token}' not exists"


class ConfigInvalid(LRBError):
    def __init__(self, config_name: str, config_value: str) -> None:
        self.config_name = config_name
        self.config_value = config_value

    def __str__(self) -> str:
        return f"Invalid config, {self.config_name} can not be {self.config_value}"


class EnvVarNotFound(LRBError):
    def __init__(self, variable_name):
        self.variable_name = variable_name

    def __str__(self) -> str:
        return f"Environment variable `{self.variable_name}` not found"


class TokenNotFound(EnvVarNotFound):
    def __str__(self) -> str:
        return f"Bot token not found, `BOT_TOKEN_ALL` or `BOT_TOKEN_{self.variable_name}` must be set in environment variables"
