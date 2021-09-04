__all__ = [
	"Token"
]

from exceptions import InvalidToken


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
		self.parts = self.str.split(self.delimiter) if self.has_delimiter else [self.str]
	
	def get(self, source: dict):
		if isinstance(source, dict):
			root, *keys = self.parts
			
			try:
				value = source[root]
			except KeyError:
				raise InvalidToken(self.str.replace(root, f"   -> {root} <-   ", 1))
			
			if len(keys) != 0:
				for index, key in enumerate(keys):
					try:
						value = value[key]
					except KeyError:
						keys[index] = f"   -> {key} <-   "
						raise InvalidToken(self.delimiter.join([root, *keys]))
			
			return value
		else:
			raise TypeError(f"source must be dictionary, not {source.__class__.__name__}")
	
	def __str__(self):
		return self.str
