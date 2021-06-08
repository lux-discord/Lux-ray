from os import getcwd, chdir
from os.path import split
from inspect import currentframe

__all__ = [
	'run_here'
]

class run_here():
	def __init__(self, target):
		target_type = target.__class__.__name__
		
		if target_type == 'str':
			self.dire_offset = target
		elif target_type == 'function':
			self.func = target
		else:
			raise TypeError(f"the 'target' must be function or str, not '{target_type}'")
		
		self.func_path = split(currentframe().f_back.f_globals['__file__'])[0]
	
	def __call__(self, *args, **kargs):
		if hasattr(self, 'dire_offset'):
			def result(*arg, **karg):
				orig_path = getcwd()
				
				chdir(self.func_path)
				chdir(self.dire_offset)
				
				f_result = args[0](*arg, **karg)
				
				chdir(orig_path)
				return f_result
		else:
			orig_path = getcwd()
			
			chdir(self.func_path)
			
			result = self.func(*args, **kargs)
			
			chdir(orig_path)
		
		return result
