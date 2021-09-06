from typing import Iterable, Union

from exceptions import InvalidToken

__all__ = [
	"Token"
]

class Token():
	def __init__(self, token: Union[str, Iterable], delimiter: str = '.'):
		if isinstance(token, str):
			self.str = token
			self.parts = token.split(delimiter)
		elif isinstance(token, Iterable):
			self.str = delimiter.join(token)
			self.parts = token
		else:
			raise TypeError(f"'token' must be string or Iterable, not {token.__class__.__name__}")
		
		if isinstance(delimiter, str):
			self.delimiter = delimiter
		else:
			self.delimiter = str(delimiter)
		
		# token may don't have delimiter even it's an Iterable(when len(token) == 1)
		self.has_delimiter = delimiter in self.str
	
	def get(self, target: dict[str]):
		root, *keys = self.parts
		
		try:
			value = target[root]
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
	
	def update(self, target: dict[str], value):
		root, *keys = self.parts
		
		if keys:
			target[root] = Token(".".join(keys)).update(target[root], value)
		else:
			target[root] = value
		
		return target
	
	def __str__(self):
		return self.str
