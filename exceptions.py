class ServerSettingNotFoundError(FileNotFoundError):
	pass

def raise_ssnfe(server_id):
	raise ServerSettingNotFoundError(f"No such server id: '{server_id}'")