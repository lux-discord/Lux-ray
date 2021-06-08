from pathlib import Path

cog_folders = [
	"lrb_backend",
	"lrb_command",
	"lrb_extension"
]
cog_folder_abbr_to_fullname = dict(zip([
	"be",
	"cmd",
	"ext"
], cog_folders))

def cog_folder_dict_generater(folder):
	"""Generate dict with gived folder
	
	Return
	------
	format: {`file.stem` : `folder_path` . `file.stem`}
	"""
	folder_path = Path(folder)
	
	return {file.stem: f"{folder_path}.{file.stem}" for file in folder_path.iterdir() if file.is_file() and file.suffix == ".py"}		

def cog_folder_loader(bot, folder):
	cog_list = cog_folder_dict_generater(folder)
	
	for file, cog in cog_list.items():
		print(f"    {file}")
		bot.load_extension(cog)
