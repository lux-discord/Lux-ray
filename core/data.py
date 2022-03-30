class BaseData():
	REQUIRE_ITEMS = []
	OPTIONAL_ITEMS = {}
	
	def __init__(self, **items):
		invalid = set(items) - {*self.REQUIRE_ITEMS, "_id"} - set(self.OPTIONAL_ITEMS)
		
		if invalid:
			raise TypeError(f"Invalid item(s): {', '.join(invalid)}")
		
		require = set(self.REQUIRE_ITEMS) - set(items)
		
		if require:
			raise ValueError(f"Require items: {', '.join(require)}")
		
		self.items = self.OPTIONAL_ITEMS | items
		self.id = items["_id"]
	
	def to_dict(self):
		return self.items

class PrefixData(BaseData):
	REQUIRE_ITEMS = [
		"prefix"
	]
	
	def __init__(self, **items):
		super().__init__(**items)
		self.prefix = items["prefix"]

class ServerData(BaseData):
	REQUIRE_ITEMS = [
		"lang_code"
	]
	OPTIONAL_ITEMS = {
		"role": []
	}
	
	def __init__(self, **items):
		super().__init__(**items)
		self.lang_code = items["lang_code"]
