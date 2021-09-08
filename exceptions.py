class LRBError(Exception):
	pass

# emoji error
class EmojiError(LRBError):
	pass

class InvalidEmojiError(EmojiError):
	def __str__(self) -> str:
		return f"'{self.args[0]}' is not a valid emoji"

# prefix error
class PrefixError(LRBError):
	pass

class PrefixNotChange(PrefixError):
	pass

class InvalidPrefix(PrefixError):
	def __str__(self) -> str:
		return f"Invalid prefix '{self.args[0]}'"

# role error
class RoleError(LRBError):
	pass

class RoleNotChange(RoleError):
	pass

# language error
class LanguageError(LRBError):
	pass

class LanguageNotChange(LanguageError):
	pass

class LanguageNotSupport(LanguageError):
	def __str__(self):
		return f"language(code) '{self.args[0]}' not suppot"

# argument error
class InvalidArgument(LRBError):
	pass

class InvalidMessageLink(InvalidArgument):
	def __str__(self) -> str:
		return f"Invalid message link '{self.args[0]}'"

class InvalidChannelID(InvalidArgument):
	def __str__(self):
		return f"Invalid channel ID '{self.args[0]}'"

class InvalidMessageID(InvalidArgument):
	def __str__(self):
		return f"Invalid message ID '{self.args[0]}'"

class InvalidExtension(LRBError):
	def __str__(self) -> str:
		return f"Invalid extension '{self.args[0]}'"

class InvalidToken(InvalidArgument):
	def __init__(self, *args: object, **kargs) -> None:
		super().__init__(*args)
		self.kargs = kargs
	
	def __str__(self) -> str:
		file_name = __file__.split('\\')[-1][:-2]
		self_name = self.__class__.__name__
		token_str = self.kargs.get("token", self.kargs.get("token_str", None))
		invalid_key = self.kargs.get("key")
		delimiter = self.kargs.get("delimiter")
		
		if not token_str:
			raise ValueError("No token(str) input")
		
		if not invalid_key:
			raise ValueError("No invalid key input")
		
		if not delimiter:
			raise ValueError("No delimiter input")
		
		return f"{token_str}\n{' '*(len(file_name)+len(self_name)+3+len(delimiter))}{'^'*len(invalid_key)}"
		# why +3 when repeating " ":
		# 1 for '.' betwean file name and self name
		# 2 for ': ' after self name
