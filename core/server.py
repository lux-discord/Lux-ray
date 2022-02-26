from exceptions import InvalidPrefix


class ServerBase():
	def __init__(self, server_data: dict) -> None:
		self.id = server_data["id"] if not (server_id := server_data.get("_id")) else server_id
		self.lang_code = server_data["lang_code"]

class Server(ServerBase):
	"""Preview"""
	def __init__(self, server_data: dict) -> None:
		super().__init__(server_data)
