from importlib import import_module


def import_from_path(import_path: str):
	module, name = import_path.rsplit(".", 1)
	return getattr(import_module(module), name)
