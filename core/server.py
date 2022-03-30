from core.data import ServerData


class Server():
	def __init__(self, server_data: ServerData) -> None:
		self.items = server_data.items
		self.id = server_data.id
		self.lang_code = server_data.lang_code
		self.role = server_data.role
	
	def update(self, **update):
		"""
		Generatr a ServerData with self.items and gived update
		
		Return
		------
		A ServerData instance base on self.items and update
		
		Return type
		-----------
		`core.data.ServerData`
		"""
		return ServerData.from_items(self.items | update)
