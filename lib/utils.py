import pathlib

def mkdirp(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)