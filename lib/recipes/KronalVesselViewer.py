import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf
from lib.recipes import Receipt

class KronalVesselViewer(Receipt):
    depends = ["ClickThroughBlocker", "ToolbarControl", "KAS"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("KronalVesselViewer" ))
        self.source_dir.output = project_dir.joinpath("GameData","KronalVesselViewer", "Plugins", "KronalVesselViewer.dll")
        self.target_dir = game_dir.joinpath("GameData", "KronalVesselViewer")
        self.kas_lib = project_dir.parent.joinpath("KAS", "LEGACY", "Plugins", "KAS.dll")
        self.clickthrouh_lib = project_dir.parent.joinpath("ClickThroughBlocker", "GameData", "000_ClickThroughBlocker", "Plugins", "ClickThroughBlocker.dll")
        self.toolbarcontrol_lib = project_dir.parent.joinpath("ToolbarControl", "GameData", "001_ToolbarControl", "Plugins", "ToolbarControl.dll")

    def build(self):
        logging.info("  Build Release API")
        self.source_dir.ensure_dir("obj")
        self.source_dir.resgen(src="Properties/Resources.resx",
                               dest="obj/KronalVesselViewer.Properties.Resources.resources")
        self.source_dir.std_compile(
            exclude=["Assembly*.cs", "KSVersion.cs"],
            references=["Assembly-CSharp.dll", 
                        "Assembly-CSharp-firstpass.dll", 
                        "UnityEngine.dll", 
                        "UnityEngine.CoreModule.dll", 
                        "UnityEngine.AssetBundleModule.dll",
                        "UnityEngine.IMGUIModule.dll",
                        "UnityEngine.ImageConversionModule.dll",
                        "UnityEngine.InputLegacyModule.dll", 
                        "UnityEngine.PhysicsModule.dll",
                        "UnityEngine.TextRenderingModule.dll",
                        "UnityEngine.UnityWebRequestWWWModule.dll",                        
                        "UnityEngine.UI.dll", self.clickthrouh_lib, self.toolbarcontrol_lib])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "KronalVesselViewer"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
