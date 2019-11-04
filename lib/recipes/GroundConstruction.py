import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf
from lib.recipes import Receipt


class GroundConstruction(Receipt):
    depends = ["AT_Utils", "ConfigurableContainers",
               "MultiAnimators", "ModuleManager"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir)
        self.source_dir.output = self.project_dir.joinpath(
            "GameData", "GroundConstruction", "Plugins", "GroundConstruction.dll")
        self.target_dir = game_dir.joinpath("GameData", "GroundConstruction")
        self.at_utils_lib = project_dir.parent.joinpath(
            "AT_Utils", "GameData", "000_AT_Utils", "Plugins", "000_AT_Utils.dll")
        self.at_utils_ui_lib = project_dir.parent.joinpath(
            "AT_Utils", "GameData", "000_AT_Utils", "Plugins", "0_00_AT_Utils_UI.dll")
        self.multianimators_lib = project_dir.parent.joinpath(
            "MultiAnimators", "obj", "002_MultiAnimators.dll")

    def build(self):
        logging.info("  Build Release API")
        self.source_dir.std_compile(
            exclude=[
                "OneTimeResourceConverter.cs",
                "Properties/AssemblyInfo-OTRC.cs",
                "WorkshopModel/ProtoGroundWorkshop.cs",
            ],
            references=["Assembly-CSharp.dll", 
                        "Assembly-CSharp-firstpass.dll", 
                        "UnityEngine.dll", 
                        "UnityEngine.CoreModule.dll",                         
                        "UnityEngine.IMGUIModule.dll", 
                        "UnityEngine.PhysicsModule.dll",
                        "UnityEngine.UI.dll", self.at_utils_lib, self.at_utils_ui_lib, self.multianimators_lib])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "GroundConstruction"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
