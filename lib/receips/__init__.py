import importlib

class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir


def find_receipt(name, game_dir, project_dir):
    module = importlib.import_module("%s.%s" % (__name__, name))
    receipt = getattr(module, name)
    return receipt(game_dir, project_dir)

