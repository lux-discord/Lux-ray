from datetime import date, timedelta


class BaseData:
    REQUIRE_ITEMS = []
    OPTIONAL_ITEMS = []

    def __init__(self, **items) -> None:
        # Valid check
        invalid = set(items) - set(self.REQUIRE_ITEMS) - set(self.OPTIONAL_ITEMS)

        if invalid:
            raise TypeError(f"Invalid item(s): {', '.join(invalid)}")

        # Require check
        require = set(self.REQUIRE_ITEMS) - set(items)

        if require:
            raise ValueError(f"Require items: {', '.join(require)}")

        self.__items = items

    @property
    def items(self):
        return self.__items

    @classmethod
    def from_items(cls, items: dict):
        return cls(**items)

    def to_dict(self):
        return self.__items


class IdBaseData(BaseData):
    def __init__(self, **items) -> None:
        self.REQUIRE_ITEMS.append("_id")
        super().__init__(**items)
        self.__id = items["_id"]

    @property
    def id(self):
        return self.__id


class PrefixData(IdBaseData):
    REQUIRE_ITEMS = ["prefix"]

    def __init__(self, **items):
        super().__init__(**items)
        self.__prefix = self.items["prefix"]

    @property
    def prefix(self):
        return self.__prefix


class ServerData(IdBaseData):
    REQUIRE_ITEMS = ["lang_code"]
    OPTIONAL_ITEMS = [
        "keywords",
        "role",
        "channel",
        "message",
    ]

    def __init__(self, **items):
        super().__init__(**items)
        self.__lang_code: str = items["lang_code"]
        self.__keywords: dict[str, str] = items.get("keywords", {})
        self.__role = RoleData.from_items(items.get("role", {}))
        self.__channel = ChannelData.from_items(items.get("channel", {}))
        self.__message = MessageData.from_items(items.get("message", {}))

    @property
    def lang_code(self):
        return self.__lang_code

    @property
    def keywords(self):
        return self.__keywords

    @property
    def role(self):
        return self.__role

    @property
    def channel(self):
        return self.__channel

    @property
    def message(self):
        return self.__message


class RoleData(BaseData):
    OPTIONAL_ITEMS = ["admin", "member", "auto"]

    def __init__(self, **items):
        super().__init__(**items)
        self.__admin: list[int] = items.get("admin", [])
        self.__member: list[int] = items.get("member", [])
        self.__auto: list[int] = items.get("auto", [])

    @property
    def admin(self):
        return self.__admin

    @property
    def member(self):
        return self.__member

    @property
    def auto(self):
        return self.__auto


class ChannelData(BaseData):
    OPTIONAL_ITEMS = [
        "category_request",
        "channel_request",
        "member_join",
        "member_leave",
    ]

    def __init__(self, **items):
        super().__init__(**items)
        self.__category_request: int = items.get("category_request", 0)
        self.__channel_request: int = items.get("channel_request", 0)
        self.__member_join: int = items.get("member_join", 0)
        self.__member_leave: int = items.get("member_leave", 0)

    @property
    def category_request(self):
        return self.__category_request

    @property
    def channel_request(self):
        return self.__channel_request

    @property
    def member_join(self):
        return self.__member_join

    @property
    def member_leave(self):
        return self.__member_leave


class MessageData(BaseData):
    OPTIONAL_ITEMS = ["listen"]

    def __init__(self, **items):
        super().__init__(**items)
        self.__listen: bool = items.get("listen", False)

    @property
    def listen(self):
        return self.__listen


class UserData(IdBaseData):
    OPTIONAL_ITEMS = ["last_login", "login_days"]

    def __init__(self, **items):
        super().__init__(**items)
        self.__last_login: str = items.get(
            "last_login", str(date.today() - timedelta(days=1))
        )
        self.__login_days: int = items.get("login_days", 0)

    @property
    def last_login(self):
        return self.__last_login

    @property
    def login_days(self):
        return self.__login_days
