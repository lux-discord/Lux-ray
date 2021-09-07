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
	
	def dict_get(self, target: dict[str]):
		try:
			sub_target = target[self.parts[0]]
			
			for key in self.parts[1:]:
				sub_target = sub_target[key]
			return sub_target
		except KeyError as e:
			raise InvalidToken(token=self.str, key=e.args[0], delimiter=self.delimiter)
	
	def dict_update(self, target: dict[str], value):
		try:
			sub_target = target[self.parts[0]]
			
			for key in self.parts[1:-1]:
				sub_target = sub_target[key]
			
			sub_target[self.parts[-1]] = value
			return target
		except KeyError as e:
			raise InvalidToken(token=self.delimiter.join(self.parts), key=e.args[0], delimiter=self.delimiter)
	
	def __str__(self):
		return self.str
