import logging
import shutil
from lib.exec import SourceDir
from lib.utils import rm_rf, mkdir_p

class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("SCANsat"))
        self.source_unity_dir = SourceDir(game_dir, project_dir.joinpath("SCANsat.Unity"))
        self.target_dir = game_dir.joinpath("GameData", "SCANsat")

    def build(self):
        plugins_dir = self.project_dir.joinpath("SCANassets", "Plugins")
        mkdir_p(plugins_dir)
        self.source_dir.output = plugins_dir.joinpath("SCANsat.dll")
        self.source_unity_dir.output = plugins_dir.joinpath("SCANsat.Unity.dll")
        self.source_unity_dir.std_compile(
            references=["UnityEngine.dll", "UnityEngine.UI.dll"])
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "UnityEngine.dll", "UnityEngine.UI.dll", self.source_unity_dir.output])

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath("SCANassets"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
