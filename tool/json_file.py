from json import load, dump

__all__ = [
	"load_file",
	"dump_file"
]

def load_file(file_path) -> dict:
	with open(file_path, "r", encoding = "UTF-8") as file:
		return load(file)

def dump_file(data, file_path, *, overwrite = False):
	with open(file_path, "w" if overwrite else "x", encoding = "UTF-8") as file:
		dump(data, file, indent = "	")
