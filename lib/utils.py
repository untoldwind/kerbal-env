import pathlib


def mkdir_p(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def rm(dir, glob):
    for file in pathlib.Path(dir).glob(glob):
        file.unlink()

def rm_rf(dir):
    path = pathlib.Path(dir)
    if not path.exists():
        return
    if path.is_file():
        path.unlink()
        return
    for child in path.iterdir():
       rm_rf(child)
    path.rmdir()

def exists(dir):
    return pathlib.Path(dir).exists()


def ln_s(source, target):
    pathlib.Path(target).symlink_to(source)
