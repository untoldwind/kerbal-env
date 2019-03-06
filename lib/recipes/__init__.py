import importlib

class Receipt:
    def __init__(self, game_dir, project_dir, depends = []):
        self.game_dir = game_dir
        self.project_dir = project_dir
        self.depends = depends

def find_receipt(name, game_dir, project_dir):
    module = importlib.import_module("%s.%s" % (__name__, name))
    receipt = getattr(module, name)
    return receipt(game_dir, project_dir)

def find_dependencies(name):
    module = importlib.import_module("%s.%s" % (__name__, name))
    receipt = getattr(module, name)
    if hasattr(receipt, "depends"):
        return getattr(receipt, "depends")
    return []
