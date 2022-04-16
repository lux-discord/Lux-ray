from functools import cache
from json import dump, load

__all__ = ["load_file", "dump_file"]


@cache
def load_file(file_path):
    with open(file_path, "r", encoding="UTF-8") as file:
        return load(file)


@cache
def dump_file(data, file_path, *, overwrite=False):
    with open(file_path, "w" if overwrite else "x", encoding="UTF-8") as file:
        dump(data, file, indent="	")
