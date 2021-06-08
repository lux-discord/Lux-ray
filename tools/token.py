from posixpath import split
from typing import Any


class Token():
	def __init__(self, token: str, delimiter: str = '.'):
		self.str = token
		self.delimiter = delimiter
		self.has_delimiter = True if delimiter in token else False
	
	def split(self, maxsplit: int = None):
		return [Token(token) for token in self.str.split(self.delimiter, maxsplit)] if maxsplit else [Token(token) for token in self.str.split(self.delimiter)]
	
	def __str__(self):
		return self.str

def get_data_with_token(data: dict, token: Token) -> Any:
	for key in token.split():
		data = data[key.str]
	
	return data

def edit_data_with_token(data: dict, token: Token, value):
	def edit(data: dict, token: Token, value):
		if token.has_delimiter:
			root, token = token.split(1)
			
			data[root.str] = edit(data[root.str], token, value)
		else:
			data[token.str] = value

		return data
	
	return edit(data, token, value)
