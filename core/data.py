from datetime import date, timedelta


class BaseData:
    REQUIRE_ITEMS = []
    OPTIONAL_ITEMS = []

    def __init__(self, **items):
        # Valid check
        invalid = set(items) - {*self.REQUIRE_ITEMS, "_id"} - set(self.OPTIONAL_ITEMS)

        if invalid:
            raise TypeError(f"Invalid item(s): {', '.join(invalid)}")

        # Require check
        require = set(self.REQUIRE_ITEMS) - set(items)

        if require:
            raise ValueError(f"Require items: {', '.join(require)}")

        self.__items = items
        self.__id: int = items["_id"]

    @property
    def items(self):
        return self.__items

    @property
    def id(self):
        return self.__id

    @classmethod
    def from_items(cls, items: dict):
        return cls(**items)

    def to_dict(self):
        return self.__items


class PrefixData(BaseData):
    REQUIRE_ITEMS = ["prefix"]

    def __init__(self, **items):
        super().__init__(**items)
        self.__prefix = self.items["prefix"]

    @property
    def prefix(self):
        return self.__prefix


class ServerData(BaseData):
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
        self.__role = RoleData(items.get("role", {}))
        self.__channel = ChannelData(items.get("channel"), {})
        self.__message = MessageData(items.get("message"), {})

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
    OPTIONAL_ITEMS = ["member_join", "member_leave"]

    def __init__(self, **items):
        super().__init__(**items)
        self.__member_join = items.get("member_join", 0)
        self.__member_leave = items.get("member_leave", 0)

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


class UserData(BaseData):
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
