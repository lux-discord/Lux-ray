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

        self._items: dict[str, Any] = self.OPTIONAL_ITEMS | items
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
    OPTIONAL_ITEMS = {
        "role": {"admin": [], "mod": [], "member": [], "auto_role": []},
        "channel": {"on_member_join": 0, "on_member_leave": 0},
        "keyword": {"replys": {}, "aliases": {}},
    }

    def __init__(self, **items):
        super().__init__(**items)
        self._lang_code: str = self.items["lang_code"]
        self._role: dict[str, list] = self.items["role"]
        self._keyword: dict[str, dict[str, str]] = self.items["keyword"]

    @property
    def lang_code(self):
        return self._lang_code

    @property
    def role(self):
        return self._role

    @property
    def role_admin(self):
        return self._role["admin"]

    @property
    def role_mod(self):
        return self._role["mod"]

    @property
    def role_member(self):
        return self._role["member"]

    @property
    def role_auto(self):
        return self._role["auto_role"]

    @property
    def keyword(self):
        return self._keyword

    @property
    def keyword_replys(self):
        return self._keyword["replys"]

    @property
    def keyword_aliases(self):
        return self._keyword["aliases"]
