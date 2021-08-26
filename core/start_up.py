from json import load

def load_start_up_message():
	with open("core/start_up_message.json", "r", encoding="UTF-8") as f:
		return load(f)

def get_bot_data(status):
	with open("core/bot_data.json", "r", encoding="UTF-8") as f:
		bot_data = load(f)
	
	bot_data["token"] = bot_data["token"][status]
	return bot_data
