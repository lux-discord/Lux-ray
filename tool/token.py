from typing import Any

__all__ = [
	"Token",
	"token_edit_data"
]

class Token():
	def __init__(self, token: str, delimiter: str = '.'):
		if isinstance(token, str):
			self.str = token
		else:
			raise TypeError(f"the token must be string, not {token.__class__.__name__}")
		
		if isinstance(delimiter, str):
			self.delimiter = delimiter
		else:
			raise TypeError(f"the delimiter must be string, not {delimiter.__class__.__name__}")
		
		self.has_delimiter = delimiter in token
	
	def split(self, maxsplit: int = 0):
		"""split Token like str.split()
		
		Parameter
		---------
		maxsplit:
			Maximum number of splits to do. 0 (the default value) means no limit.
		"""
		return [Token(token) for token in str(self).split(self.delimiter, maxsplit - 1)]
	
	def split_to_str(self, maxsplit: int=0):
		return self.str.split(self.delimiter, maxsplit - 1)
	
	def get(self, source: dict):
		for key in self.split_to_str():
			try:
				data = data[key]
			except NameError:
				data = source[key]
		
		return data
	
	def __str__(self):
		return self.str

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
