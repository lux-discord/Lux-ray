class LRBError(Exception):
	pass

class EmojiError(LRBError):
	pass

class InvalidEmojiError(EmojiError):
	def __init__(self, raw_emoji) -> None:
		self.raw_emoji = raw_emoji
	
	def __str__(self) -> str:
		return f"'{self.raw_emoji}' is not a valid emoji"

class PrefixError(LRBError):
	pass

class PrefixNotChange(PrefixError):
	pass

class PrefixInvalid(PrefixError):
	def __init__(self, prefix):
		self.prefix = prefix
	
	def __str__(self) -> str:
		return f"Invalid prefix '{self.prefix}'"

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
	def __init__(self, lang_code):
		self.lang_code = lang_code
	
	def __str__(self):
		return f"language(code) '{self.lang_code}' not suppot"

class InvalidArgument(LRBError):
	pass

class InvalidMessageLink(InvalidArgument):
	def __init__(self, link) -> None:
		self.link = link
	
	def __str__(self) -> str:
		return f"Invalid message link '{self.link}'"

class InvalidChannelID(InvalidArgument):
	def __init__(self, id):
		self.id = id
	
	def __str__(self):
		return f"Invalid channel ID '{self.id}'"

class InvalidMessageID(InvalidArgument):
	def __init__(self, id):
		self.id = id
	
	def __str__(self):
		return f"Invalid message ID '{self.id}'"

class InvalidExtension(LRBError):
	def __init__(self, extension_name):
		self.extension_name = extension_name
	
	def __str__(self) -> str:
		return f"Invalid extnesion '{self.extension_name}'"
