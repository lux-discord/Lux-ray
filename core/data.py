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

        self._items = items
        self._id: int = items["_id"]

    @property
    def items(self):
        return self._items

    @property
    def id(self):
        return self._id

    @classmethod
    def from_items(cls, items: dict):
        return cls(**items)

    def to_dict(self):
        return self.items


class PrefixData(BaseData):
    REQUIRE_ITEMS = ["prefix"]

    def __init__(self, **items):
        super().__init__(**items)
        self._prefix = self.items["prefix"]

    @property
    def prefix(self):
        return self._prefix


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
        self._lang_code: str = items["lang_code"]
        self._listen_message: bool = items.get("listen_message", False)
        self._role: dict[str, list[int]] = items.get(
            "role", {"admin": [], "mod": [], "member": [], "auto_role": []}
        )
        self._channel: dict[str, int] = items.get(
            "channel", {"on_member_join": 0, "on_member_leave": 0}
        )
        self._keywords: dict[str, str] = items.get("keywords", {})

    @property
    def lang_code(self):
        return self._lang_code

    @property
    def listen_message(self):
        return self._listen_message

    @property
    def role(self):
        return self._role

    @property
    def role_member(self):
        return self._role.get("member", []) if self._role else None

    @property
    def role_auto(self):
        return self._role.get("auto", []) if self._role else None

    @property
    def channel(self):
        return self._channel

    @property
    def keywords(self):
        return self._keywords


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
