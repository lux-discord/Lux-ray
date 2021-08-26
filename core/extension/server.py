from discord.ext.commands.context import Context

from ..cog import cog_folder_abbr_to_fullname
from ..db import bot_db, extension_server_db
from ..language import LANG_FILE_PATH, Language
from ..server import Server, ServerBasic

extension_coll = bot_db["extension"]

class ExtensionServer(ServerBasic):
	def __init__(self, ctx: Context) -> None:
		if not isinstance(ctx, Context):
			raise TypeError(f"ctx must be discord.ext.commands.Context, not {ctx.__class__.__name__}")
		
		id = ctx.guild.id
		extension_name: str = ctx.invoked_parents[0]
		extension_data: dict = extension_coll.find_one({"name": extension_name})
		extension_server_coll = extension_server_db[extension_name]
		
		super().__init__(extension_server_coll)
		
		id = ctx.guild.id
		if not (extension_server_data := self.server_coll.find_one({"server_id": id})):
			extension_server_data = {
				"server_id": id,
				"lang_code": "en"
			}
			self.server_coll.insert_one(extension_server_data)
		
		self.__ctx = ctx
		self.id = id
		self.data = extension_server_data
		self.lang_code = extension_server_data["lang_code"]
		self.language = Language(self.lang_code, extension_data["support_language"], "/".join([
			cog_folder_abbr_to_fullname["ext"],
			extension_name,
			extension_data.get("lang_file_path", LANG_FILE_PATH)
		]))
	
	def MainServer(self):
		return Server(self.__ctx)
