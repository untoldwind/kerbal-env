import logging
import shutil
from lib.exec import run_command, SourceDir
from lib.utils import mkdir_p, rm_rf, rm

class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("X-Science"))
        self.source_dir.output = project_dir.joinpath("X-Science", "GameData", "[x] Science!", "[x] Science!.dll")
        self.target_dir = game_dir.joinpath("GameData", "[x] Science!")

    def build(self):
        logging.info("  Build Release")
        rm(self.project_dir.joinpath("X-Science", "GameData", "[x] Science!"), "*.dll")
        self.source_dir.resources = ["icons/%s,ScienceChecklist.icons.%s" % (icon.name, icon.name) for icon in self.source_dir.joinpath("icons").glob("*.png")]
        self.source_dir.std_compile(
            exclude="docs_project/**/*.cs",
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "X-Science", "GameData", "[x] Science!"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
