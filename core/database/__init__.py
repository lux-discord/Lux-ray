from .mongodb import MongoDB

_DRIVERS = {"mongodb": MongoDB}


def get_driver(database_type: str):
    database_type = database_type.lower()

    try:
        return _DRIVERS[database_type]
    except KeyError:
        raise ValueError(f"Not support storage type `{database_type}`")
