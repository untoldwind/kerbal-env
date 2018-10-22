import pathlib
import logging

def mkdir_p(path):
    logging.debug("Creating path: %s" % path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def rm(dir, glob):
    for file in pathlib.Path(dir).glob(glob):
        logging.debug("Deleting file: %s" % file)
        file.unlink()

def rm_rf(dir):
    path = pathlib.Path(dir)
    if not path.exists():
        return
    if path.is_file():
        logging.debug("Deleting file: %s" % path)
        path.unlink()
        return
    for child in path.iterdir():
       rm_rf(child)
    logging.debug("Deleting dir: %s" % path)
    path.rmdir()

def ln_s(source, target):
    logging.debug("Creating symlink %s -> %s" % (source, target))
    pathlib.Path(target).symlink_to(source)
