from disnake.ext.commands.context import Context

from ..language import PUBLIC_LANGUAGE_DIR, Language
from ..server import Server, ServerBase


class ExtensionServer(ServerBase):
	def __init__(self, ctx: Context) -> None:
		if not isinstance(ctx, Context):
			raise TypeError(f"ctx must be discord.ext.commands.Context, not {ctx.__class__.__name__}")
		
		extension_name: str = ctx.invoked_parents[0]
		extension_server_coll = extension_server_db[extension_name]
		
		super().__init__(ctx, extension_server_coll)
		
		extension_manifest: dict = extension_coll.find_one({"name": extension_name})
		
		if not (extension_server_data := self.server_coll.find_one({"_id": self.id})):
			extension_server_data = {
				"_id": self.id,
				"lang_code": "en"
			}
			self.server_coll.insert_one(extension_server_data)
		
		self.data = extension_server_data
		self.lang_code = extension_server_data["lang_code"]
		self.language = Language(self.lang_code, extension_manifest["support_language"], "/".join([
			cog_folder_abbr_to_fullname["ext"],
			extension_name,
			extension_manifest.get("lang_file_path", PUBLIC_LANGUAGE_DIR)
		]))
	
	def MainServer(self):
		return Server(self.ctx)
