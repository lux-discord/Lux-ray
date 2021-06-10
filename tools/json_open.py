from json import load, dump

__all__ = [
	"json_load",
	"json_dump"
]

def json_load(file_path):
	with open(file_path, "r", encoding = "UTF-8") as file:
		return load(file)

def json_dump(data, file_path, *, overwrite = False):
	with open(file_path, "w" if overwrite else "x", encoding = "UTF-8") as file:
		dump(data, file, indent = "	")
