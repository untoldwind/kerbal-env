import logging
import shutil
from lib.exec import run_command, SourceDir
from lib.utils import mkdir_p, rm_rf, rm
from lib.recipes import Receipt

class SpaceTuxLibrary(Receipt):
    depends = ["ClickThroughBlocker", "ToolbarControl"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir_log = SourceDir(game_dir, project_dir.joinpath("KSP_Log"))
        self.source_dir_log.output = project_dir.joinpath("GameData", "SpaceTuxLibrary", "Plugins", "KSP_Log.dll")
        self.source_dir_colorpicker = SourceDir(game_dir, project_dir.joinpath("KSP_ColorPicker"))
        self.source_dir_colorpicker.output = project_dir.joinpath("GameData", "SpaceTuxLibrary", "Plugins", "KSP_ColorPicker.dll")
        self.source_dir_parthighlighter = SourceDir(game_dir, project_dir.joinpath("KSP_PartHighlighter"))
        self.source_dir_parthighlighter.output = project_dir.joinpath("GameData", "SpaceTuxLibrary", "Plugins", "KSP_PartHighlighter.dll")
        self.target_dir = game_dir.joinpath("GameData", "SpaceTuxLibrary")
        self.clickthrouh_lib = project_dir.parent.joinpath("ClickThroughBlocker", "GameData", "000_ClickThroughBlocker", "ClickThroughBlocker.dll")
        self.toolbarcontrol_lib = project_dir.parent.joinpath("ToolbarControl", "GameData", "001_ToolbarControl", "ToolbarControl.dll")

    def build(self):
        logging.info("  Build Release KSP_Log")
        rm(self.project_dir.joinpath("GameData", "SpaceTuxLibrary", "Plugins"), "*.dll")
        mkdir_p(self.project_dir.joinpath("GameData", "SpaceTuxLibrary", "Plugins"));
        self.source_dir_log.std_compile(
            exclude="docs_project/**/*.cs",
            references=["Assembly-CSharp.dll", 
                        "Assembly-CSharp-firstpass.dll", 
                        "UnityEngine.dll",
                        "UnityEngine.CoreModule.dll",
                        "UnityEngine.UI.dll"])
        logging.info("  Build Release KSP_ColorPicker")
        self.source_dir_colorpicker.std_compile(
            exclude="docs_project/**/*.cs",
            references=[self.source_dir_log.output,
                        self.clickthrouh_lib,
                        self.toolbarcontrol_lib,
                        "Assembly-CSharp.dll", 
                        "Assembly-CSharp-firstpass.dll", 
                        "UnityEngine.dll",
                        "UnityEngine.CoreModule.dll",
                        "UnityEngine.IMGUIModule.dll",
                        "UnityEngine.InputLegacyModule.dll", 
                        "UnityEngine.UI.dll"])
        logging.info("  Build Release KSP_PartHighlighter")
        self.source_dir_parthighlighter.std_compile(
            exclude="docs_project/**/*.cs",
            references=[self.source_dir_log.output,
                        "Assembly-CSharp.dll", 
                        "Assembly-CSharp-firstpass.dll", 
                        "UnityEngine.dll",
                        "UnityEngine.CoreModule.dll",
                        "UnityEngine.UI.dll"])

    def can_install(self):
        return self.source_dir_log.output.exists() and self.source_dir_colorpicker.output.exists() and self.source_dir_parthighlighter.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "SpaceTuxLibrary"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
