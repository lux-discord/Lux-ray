from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


class BaseData:
    REQUIRE_ITEMS = []
    OPTIONAL_ITEMS = {}

    def __init__(self, **items):
        # Valid check
        invalid = set(items) - {*self.REQUIRE_ITEMS, "_id"} - set(self.OPTIONAL_ITEMS)

        if invalid:
            raise TypeError(f"Invalid item(s): {', '.join(invalid)}")

        # Require check
        require = set(self.REQUIRE_ITEMS) - set(items)

        if require:
            raise ValueError(f"Require items: {', '.join(require)}")

        self.items: dict[str, Any] = self.OPTIONAL_ITEMS | items
        self.id: int = items["_id"]

    @classmethod
    def from_items(cls, items: dict):
        return cls(**items)

    def to_dict(self):
        return self.items


class PrefixData(BaseData):
    REQUIRE_ITEMS = ["prefix"]

    def __init__(self, **items):
        super().__init__(**items)
        self.prefix = self.items["prefix"]


class ServerData(BaseData):
    REQUIRE_ITEMS = ["lang_code"]
    OPTIONAL_ITEMS = {
        "role": {"admin": [], "mod": [], "member": [], "auto_role": []},
        "channel": {"on_member_join": int(), "on_member_leave": int()},
        "keyword": {"replys": [], "aliases": {}},
    }

    def __init__(self, **items):
        super().__init__(**items)
        self.lang_code: str = self.items["lang_code"]
        self.role: dict = self.items["role"]
        self.keyword: dict = self.items["keyword"]
