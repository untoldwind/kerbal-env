from lib.receips import Receipt

class KramaxPluginReload(Receipt):
    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)

    def build(self):
        pass

    def can_install(self):
        return True

    def install(self):
        pass

    def check_installed(self):
        return False
