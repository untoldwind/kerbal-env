import shutil
from lib.recipes import Receipt
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf, rm

class KramaxPluginReload(Receipt):
    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.plugin_dir = project_dir.joinpath("GameData", "KramaxPluginReload", "Plugins")
        self.source_dir = SourceDir(game_dir, project_dir)
        self.source_dir.output = self.plugin_dir.joinpath("KramaxPluginReload.dll")
        self.source_dir_extensions = SourceDir(game_dir, project_dir.joinpath("KramaxReloadExtensions" ))
        self.source_dir_extensions.output = self.plugin_dir.joinpath("KramaxReloadExtensions.dll")
        self.target_dir = game_dir.joinpath("GameData", "KramaxPluginReload")

    def build(self):
        rm(self.plugin_dir, "*.dll")
        rm(self.plugin_dir, "*.pdb")
        self.source_dir_extensions.std_compile(
            exclude="ReleaseReloadableMonoBehaviour.cs",
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])
        self.source_dir.std_compile(
            exclude="KramaxReloadExtensions/**/*|ReleaseReloadableMonoBehaviour.cs",
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll", self.source_dir_extensions.output])

    def can_install(self):
        return self.source_dir.output.exists() and self.source_dir_extensions.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "KramaxPluginReload"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
