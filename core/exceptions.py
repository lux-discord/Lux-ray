from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional


class LRBError(Exception):
    """
    Base exception of Lux-ray bot
    """

    def __init__(self, message: "Optional[str]" = None, *args: object) -> None:
        super().__init__(message, *args)


class DatabaseError(LRBError):
    def __init__(self, operate) -> None:
        # TODO better error message
        super().__init__(f"Operate `{operate}` failure")
