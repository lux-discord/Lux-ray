from typing import Callable


event_processes: dict[str, list[Callable]] = {}

def bg_register(event: str, *processes: Callable):
	try:
		event_processes[event].extend(processes)
	except KeyError:
		event_processes[event] = list(processes)

def load_bg(bot):
	for event_name, processes in event_processes.items():
		async def event(*args, **kargs):
			for process in processes:
				process(*args, **kargs)
		
		bot.add_listener(event, event_name)
