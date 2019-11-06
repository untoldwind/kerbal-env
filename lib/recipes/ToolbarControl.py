import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf
from lib.recipes import Receipt

class ToolbarControl(Receipt):
    depends = ["ClickThroughBlocker"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("ToolbarControl" ))
        self.source_dir.output = project_dir.joinpath("GameData","001_ToolbarControl", "Plugins", "ToolbarControl.dll")
        self.target_dir = game_dir.joinpath("GameData", "001_ToolbarControl")
        self.clickthrouh_lib = project_dir.parent.joinpath("ClickThroughBlocker", "GameData", "000_ClickThroughBlocker", "Plugins", "ClickThroughBlocker.dll")

    def build(self):
        logging.info("  Build Release API")
        mkdir_p(self.project_dir.joinpath("GameData", "001_ToolbarControl", "Plugins"));
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", 
                        "Assembly-CSharp-firstpass.dll", 
                        "UnityEngine.dll", 
                        "UnityEngine.CoreModule.dll", 
                        "UnityEngine.AnimationModule.dll",
                        "UnityEngine.ImageConversionModule.dll",
                        "UnityEngine.IMGUIModule.dll",
                        "UnityEngine.InputLegacyModule.dll", 
                        "UnityEngine.UI.dll", self.clickthrouh_lib])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "001_ToolbarControl"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
