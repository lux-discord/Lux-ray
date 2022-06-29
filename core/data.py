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

        self.items = items

    @classmethod
    def from_items(cls, items: dict):
        return cls(**items)

    def to_dict(self):
        return self.items


class IdBaseData(BaseData):
    def __init__(self, **items) -> None:
        self.REQUIRE_ITEMS.append("_id")
        super().__init__(**items)
        self.id = items["_id"]


class PrefixData(IdBaseData):
    REQUIRE_ITEMS = ["prefix"]

    def __init__(self, **items):
        super().__init__(**items)
        self.prefix = self.items["prefix"]


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
        self.lang_code: str = items["lang_code"]
        self.keywords: dict[str, str] = items.get("keywords", {})
        self.role = RoleData.from_items(items.get("role", {}))
        self.channel = ChannelData.from_items(items.get("channel", {}))
        self.message = MessageData.from_items(items.get("message", {}))


class RoleData(BaseData):
    OPTIONAL_ITEMS = ["admin", "member", "auto"]

    def __init__(self, **items):
        super().__init__(**items)
        self.admin: list[int] = items.get("admin", [])
        self.member: list[int] = items.get("member", [])
        self.auto: list[int] = items.get("auto", [])


class ChannelData(BaseData):
    OPTIONAL_ITEMS = [
        "category_request",
        "channel_request",
        "requestable_category",
        "member_join",
        "member_leave",
    ]

    def __init__(self, **items):
        super().__init__(**items)
        self.category_request: int = items.get("category_request", 0)
        self.channel_request: int = items.get("channel_request", 0)
        self.requestable_category: list[int] = items.get("requestable_category", [])
        self.member_join: int = items.get("member_join", 0)
        self.member_leave: int = items.get("member_leave", 0)


class MessageData(BaseData):
    OPTIONAL_ITEMS = ["listen"]

    def __init__(self, **items):
        super().__init__(**items)
        self.listen: bool = items.get("listen", True)


class UserData(IdBaseData):
    OPTIONAL_ITEMS = ["last_login", "login_days"]

    def __init__(self, **items):
        super().__init__(**items)
        self.last_login: str = items.get(
            "last_login", str(date.today() - timedelta(days=1))
        )
        self.login_days: int = items.get("login_days", 0)
