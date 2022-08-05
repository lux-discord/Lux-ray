class BaseData:
    REQUIRE_ITEMS: list[str] = []
    OPTIONAL_ITEMS: list[str] = []

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
        self.id: int = items["_id"]


class ServerData(IdBaseData):
    REQUIRE_ITEMS = ["lang_code"]
    OPTIONAL_ITEMS = [
        "role",
        "channel",
        "message",
    ]

    def __init__(self, **items):
        super().__init__(**items)
        self.lang_code: str = items["lang_code"]
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
        "category_request_process_channel",
        "channel_request_process_channel",
        "requestable_category",
        "member_join",
        "member_leave",
    ]

    def __init__(self, **items):
        super().__init__(**items)
        self.category_request_process_channel: int = items.get(
            "category_request_process_channel", 0
        )
        self.channel_request_process_channel: int = items.get(
            "channel_request_process_channel", 0
        )
        self.requestable_category: dict[str, str] = items.get(
            "requestable_category", {}
        )
        self.member_join: int = items.get("member_join", 0)
        self.member_leave: int = items.get("member_leave", 0)


class MessageData(BaseData):
    OPTIONAL_ITEMS = [
        "keywords",
        "listen",  # deprecated
    ]

    def __init__(self, **items):
        super().__init__(**items)
        self.keywords: dict[str, str] = items.get("keywords", {})


class UserData(IdBaseData):
    OPTIONAL_ITEMS = [
        "last_login",  # deprecated
        "login_days",  # deprecated
    ]

    def __init__(self, **items):
        super().__init__(**items)
