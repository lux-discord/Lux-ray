from tomli import load


def load_file(file_path):
    with open(file_path, "rb") as f:
        return load(f)
