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
        return self.items


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
        "listen_message",
        "role",
        "channel",
        "keywords",
    ]

    def __init__(self, **items):
        super().__init__(**items)
        self.__lang_code: str = items["lang_code"]
        self.__listen_message: bool = items.get("listen_message", False)
        self.__role: dict[str, list[int]] = items.get(
            "role", {"admin": [], "mod": [], "member": [], "auto_role": []}
        )
        self.__channel: dict[str, int] = items.get(
            "channel", {"on_member_join": 0, "on_member_leave": 0}
        )
        self.__keywords: dict[str, str] = items.get("keywords", {})

    @property
    def lang_code(self):
        return self.__lang_code

    @property
    def listen_message(self):
        return self.__listen_message

    @property
    def role(self):
        return self.__role

    @property
    def role_member(self):
        return self.__role.get("member", []) if self.__role else None

    @property
    def role_auto(self):
        return self.__role.get("auto", []) if self.__role else None

    @property
    def channel(self):
        return self.__channel

    @property
    def keywords(self):
        return self.__keywords



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
