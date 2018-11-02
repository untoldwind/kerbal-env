import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf

class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("ToolbarControl" ))
        self.source_dir.output = project_dir.joinpath("GameData","001_ToolbarControl", "ToolbarControl.dll")
        self.target_dir = game_dir.joinpath("GameData", "001_ToolbarControl")
        self.clickthrouh_lib = project_dir.parent.joinpath("ClickThroughBlocker", "GameData", "000_ClickThroughBlocker", "ClickThroughBlocker.dll")

    def build(self):
        logging.info("  Build Release API")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll", self.clickthrouh_lib])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "001_ToolbarControl"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
