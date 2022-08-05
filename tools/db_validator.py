from core.config import Config

DEFAULT_SERVER_VALIDATOR = {
    "$jsonSchema": {
        "required": ["_id", "lang_code", "role", "channel"],
        "additionalProperties": False,
        "properties": {
            "_id": {"bsonType": "long"},
            "lang_code": {"bsonType": "string"},
            "role": {
                "bsonType": "object",
                "required": ["admin", "mod", "member", "auto_role"],
                "properties": {
                    "admin": {"bsonType": "array", "uniqueItems": True},
                    "mod": {"bsonType": "array", "uniqueItems": True},
                    "member": {"bsonType": "array", "uniqueItems": True},
                    "auto_role": {"bsonType": "array", "uniqueItems": True},
                },
            },
            "channel": {
                "bsonType": "object",
                "required": ["on_member_join", "on_member_leave"],
            },
            "keyword_reply": {"bsonType": "object"},
            "keyword_alias": {"bsonType": "object"},
        },
    }
}


def get_default_value():
    if not (
        config_path := input("Input a config path(Default to 'bot-config.toml'): ")
    ):
        config_path = "bot-config.toml"

    if not (
        mode := input("Input a mode(1 for 'dev' or 2 for 'stable', default 'dev'): ")
    ):
        mode = "dev"

    if not (
        coll := input(
            "Input a collection name you want set validator(Default 'server'): "
        )
    ):
        coll = "server"

    return {"config_path": config_path, "mode": mode, "coll": coll}


def setup_db(config_path, mode):
    config = Config(config_path, mode)
    db_client = config.create_database_client()
    return db_client["discord-bot"]


def update_validator(config_path=None, mode=None, coll=None, *, validator=None):
    default_value = get_default_value()

    if not config_path:
        config_path = default_value["config_path"]

    if not mode:
        mode = default_value["mode"]

    if not coll:
        coll = default_value["coll"]

    if not validator and not (
        validator := input("Input a validator(Default use DEFAULT_SERVER_VALIDATOR): ")
    ):
        validator = DEFAULT_SERVER_VALIDATOR

    db = setup_db(config_path, mode)
    print(db.command("collMod", coll, validator=validator))


def test_validator(config_path=None, mode=None, coll=None, test_doc=None):
    default_value = get_default_value()

    if not config_path:
        config_path = default_value["config_path"]

    if not mode:
        mode = default_value["mode"]

    if not coll:
        coll = default_value["coll"]

    if not test_doc:
        while True:
            if test_doc := input("Input a doc to test"):
                break
