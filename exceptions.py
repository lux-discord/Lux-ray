class LRBError(Exception):
	pass

class EmojiError(LRBError):
	pass

class InvalidEmojiError(EmojiError):
	def __str__(self) -> str:
		return f"'{self.args[0]}' is not a valid emoji"

class PrefixError(LRBError):
	pass

class PrefixNotChange(PrefixError):
	pass

class PrefixInvalid(PrefixError):
	def __str__(self) -> str:
		return f"Invalid prefix '{self.args[0]}'"

class RoleError(LRBError):
	pass

class RoleNotChange(RoleError):
	pass

class RoleTypeInvalid(RoleError):
	pass

class LanguageError(LRBError):
	pass

class LanguageNotChange(LanguageError):
	pass

class LanguageNotSupport(LanguageError):
	def __str__(self):
		return f"language(code) '{self.args[0]}' not suppot"

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
	def __str__(self) -> str:
		return f"Invalid token: '{self.args[0]}'"
