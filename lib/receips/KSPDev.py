import logging
from lib.exec import SourceDir
from lib.receips import Receipt

class KSPDev(Receipt):
    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("Sources", "Utils"))
        self.source_dir.output = project_dir.joinpath("Binaries", "KSPDev_Utils.0.37.dll")
        self.source_dir.doc_output = project_dir.joinpath("Binaries", "KSPDev_Utils.0.37.xml")

    def build(self):
        logging.info("  Build Release")
        self.source_dir.std_compile(
            exclude="docs_project/**/*.cs",
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        # Note: Will not be installed by itself
        pass

    def check_installed(self):
        # Note: Will not be installed by itself
        return True
