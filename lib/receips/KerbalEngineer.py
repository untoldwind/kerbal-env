import logging
import shutil
from lib.exec import run_command, SourceDir
from lib.utils import rm_rf, rm
from lib.receips import Receipt


class KerbalEngineer(Receipt):
    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(
            game_dir, project_dir.joinpath("KerbalEngineer"))
        self.source_dir.output = project_dir.joinpath(
            "Output", "KerbalEngineer", "KerbalEngineer.dll")
        self.source_unity_dir = SourceDir(
            game_dir, project_dir.joinpath("KerbalEngineer.Unity"))
        self.source_unity_dir.output = project_dir.joinpath(
            "Output", "KerbalEngineer", "KerbalEngineer.Unity.dll")
        self.target_dir = self.game_dir.joinpath("GameData", "KerbalEngineer")

    def build(self):
        logging.info("  Build Release")
        rm(self.project_dir.joinpath("Output", "KerbalEngineer"), "*.dll")
        self.source_unity_dir.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll", self.source_unity_dir.output])

    def can_install(self):
        return self.source_dir.output.exists() and self.source_unity_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "Output", "KerbalEngineer"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
