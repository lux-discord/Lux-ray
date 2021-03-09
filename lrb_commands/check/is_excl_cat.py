from basic_import import *

def is_excl_cat():
	'''
	full name: is_exclusive_category
	'''
	def predicate(ctx):
		ctx.channel.category
		return 
	return commands.check(predicate)
