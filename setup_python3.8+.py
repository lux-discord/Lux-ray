from subprocess import run as cli
from subprocess import DEVNULL
from os import chdir
from pathlib import Path
from requests import get as rget
from tarfile import open as topen

python_version = "3.9.12"
remote_url = f"https://www.python.org/ftp/python/{python_version}/Python-{python_version}.tgz"
locale_file = f"Python-{python_version}.tgz"
extract_path = Path(".").resolve()
extract_folder = Path(f"./Python-{python_version}")
target_folder = Path("./python").resolve()
configure_command = ["./configure", "--enable-optimizations", f"--prefix={target_folder}"]

def download():
	print(f"Downloading {locale_file}")
	print("Getting request...")
	r = rget(remote_url, allow_redirects=True)

	print("Writing file...")
	with open(locale_file, "wb") as f:
		for chunk in r.iter_content(chunk_size=1024):
			f.write(chunk)

	print("Done")

def extract():
	print(f"Extracting file to `{extract_path.resolve()}`...")
	file = topen(locale_file)
	names = file.getnames()

	for name in names:
		file.extract(name, path=extract_path)

	file.close()
	print("Done")

def configure():
	print("Configure...")
	cli(configure_command, stdout=DEVNULL)
	print("make install...")
	cli(["make", "install"], stdout=DEVNULL)
	print("Done")

def cleanup():
	print("Cleanup..")
	cli(["rm", locale_file])
	cli(["rm", "-r", extract_folder])
	print("Done")

def main():
	download()
	extract()
	chdir(extract_folder)
	configure()
	chdir("..")
	cleanup()

if __name__ == "__main__":
	main()