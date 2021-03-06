import logging
from lib.exec import SourceDir
from lib.recipes import Receipt
from lib.utils import mkdir_p

class KSPDev_Utils(Receipt):
    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("Source"))
        self.source_dir.output = project_dir.joinpath("Binaries", "KSPDev_Utils.2.3.dll")
        self.source_dir.doc_output = project_dir.joinpath("Binaries", "KSPDev_Utils.2.3.xml")
        mkdir_p(project_dir.joinpath("Binaries"))

    def build(self):
        logging.info("  Build Release")
        self.source_dir.std_compile(
            exclude="docs_project/**/*.cs",
            references=["Assembly-CSharp.dll", 
                        "Assembly-CSharp-firstpass.dll", 
                        "UnityEngine.dll", 
                        "UnityEngine.CoreModule.dll", 
                        "UnityEngine.AssetBundleModule.dll",
                        "UnityEngine.AudioModule.dll",
                        "UnityEngine.InputLegacyModule.dll",
                        "UnityEngine.PhysicsModule.dll",
                        "UnityEngine.IMGUIModule.dll",
                        "UnityEngine.TextRenderingModule.dll",
                        "UnityEngine.VehiclesModule.dll",
                        "UnityEngine.UI.dll"
                        ])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        # Note: Will not be installed by itself
        pass

    def check_installed(self):
        # Note: Will not be installed by itself
        return True
