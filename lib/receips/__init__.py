import importlib


def find_receipt(name, game_dir, project_dir):
    module = importlib.import_module("%s.%s" % (__name__, name))
    return module.Receipt(game_dir, project_dir)

