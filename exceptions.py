class LRBError(Exception):
	"""Base Exception of Lux-ray bot"""
	pass

class ParameterError(LRBError):
	pass

class NoTokenInputError(ParameterError):
	def __str__(self):
		return "No token input"

class LanguageNotSuppot(LookupError):
	def __init__(self, language):
		self.language = language
	
	def __str__(self):
		return f"{self.language} not suppot"
