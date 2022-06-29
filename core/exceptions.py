from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional


class LRBError(Exception):
    """
    Base exception of Lux-ray bot
    """

    def __init__(self, message: "Optional[str]" = None, *args: object) -> None:
        super().__init__(message, *args)


# Where should those exceptions inherit from???
class LanguageNotSupport(LRBError):
    """
    Language not support
    """

    def __init__(self, lang_code: str) -> None:
        self.lang_code = lang_code
        super().__init__(f"language(code) '{lang_code}' not suppot")


class ConfigInvalid(LRBError):
    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value
        super().__init__(f"Invalid config, {name} can not be {value}")


class DatabaseError(LRBError):
    def __init__(self, operate) -> None:
        # TODO better error message
        super().__init__(f"Operate `{operate}` failure")


# Invalid user input
class InvalidUserInput(LRBError):
    """
    Base exception of all invalid user input
    """


class InvalidMessageLink(InvalidUserInput):
    def __init__(self, msg_link: str) -> None:
        self.msg_link = msg_link
        super().__init__(f"Invalid message link '{msg_link}'")


class InvalidChannelID(InvalidUserInput):
    def __init__(self, ch_id: int):
        self.ch_id = ch_id
        super().__init__(f"Invalid channel ID '{ch_id}'")


class InvalidMessageID(InvalidUserInput):
    def __init__(self, msg_id) -> None:
        self.msg_id = msg_id
        super().__init__(f"Invalid message ID '{self.msg_id}'")
