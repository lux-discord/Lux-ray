from typing import Any

__all__ = [
	"Token",
	"token_get_data",
	"token_edit_data",
	"token_add_key",
	"token_del_key"
]

class Token():
	def __init__(self, token: str, delimiter: str = '.'):
		self.str = token
		self.delimiter = delimiter
		self.has_delimiter = True if delimiter in token else False
	
	def split(self, maxsplit: int = None):
		return [Token(token) for token in self.str.split(self.delimiter, maxsplit)] if maxsplit else [Token(token) for token in self.str.split(self.delimiter)]
	
	def __str__(self):
		return self.str

def token_get_data(data: dict, token: Token) -> Any:
	for key in token.split():
		data = data[key.str]
	
	return data

def token_edit_data(data: dict, token: Token, value, *, allow_add_key = False):
	def edit(data: dict, token: Token, value, overwrite):
		if token.has_delimiter:
			root, token = token.split(1)
			root = root.str
			
			if (root in data) or (root not in data and overwrite):
				data[root] = edit(data[root], token, value, overwrite)
			else:
				raise KeyError(f"Not allow add key({root})")
		else:
			token = token.str
			
			if (token in data) or (token not in data and overwrite):
				data[token] = value
			else:
				raise KeyError(f"Not allow add key({token})")

		return data
	
	return edit(data, token, value, allow_add_key)
