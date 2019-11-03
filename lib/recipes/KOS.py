import logging
import shutil
from lib.exec import SourceDir
from lib.utils import ln_s, rm_rf, rm
from lib.recipes import Receipt


class KOS(Receipt):
    depends=["ModuleManager"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)

    def build(self):
        src_dir = SourceDir(self.game_dir, self.project_dir.joinpath("src"))

        bin_target = self.project_dir.joinpath(
            "Resources", "GameData", "kOS", "Plugins")
        rm(bin_target, "*")

        src_dir.nuget_restore()
        src_dir.sub_dir("packages").nuget_install("NUnit.Runners", "2.6.4")
        src_dir.sub_dir("packages").nuget_install("SharpZipLib", "0.86.0")

        shutil.copy(src_dir.joinpath("packages", "SharpZipLib.0.86.0",
                                     "lib", "20", "ICSharpCode.SharpZipLib.dll"), bin_target)

        logging.info("  Build kOS.Safe")
        kos_safe_src = src_dir.sub_dir("kOS.Safe")
        kos_safe_src.output = bin_target.joinpath("kOS.Safe.dll")
        kos_safe_src.ensure_dir("obj")
        kos_safe_src.resgen(src="Properties/Resources.resx",
                                dest="obj/kOS.Safe.Properties.Resources.resources")
        kos_safe_src.std_compile(
            references=[bin_target.joinpath("ICSharpCode.SharpZipLib.dll")])

        logging.info("  Build kOS")
        kos_src = src_dir.sub_dir("kOS")
        kos_src.output = bin_target.joinpath("kOS.dll")
        kos_src.ensure_dir("obj")
        kos_src.resgen(src="Properties/Resources.resx",
                       dest="obj/kOS.Properties.Resources.resources")
        kos_src.std_compile(references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll",
                                        "UnityEngine.dll", 
                                        "UnityEngine.CoreModule.dll", 
                                        "UnityEngine.AnimationModule.dll",
                                        "UnityEngine.AudioModule.dll",
                                        "UnityEngine.InputLegacyModule.dll",
                                        "UnityEngine.ImageConversionModule.dll",
                                        "UnityEngine.PhysicsModule.dll",
                                        "UnityEngine.UI.dll",
                                        "UnityEngine.IMGUIModule.dll",
                                        "UnityEngine.TextRenderingModule.dll",
                                        "UnityEngine.UnityWebRequestAudioModule.dll",
                                        "UnityEngine.UnityWebRequestModule.dll",
                                        "UnityEngine.UnityWebRequestWWWModule.dll",
                                         kos_safe_src.output])

        logging.info("  Build kOS.Safe.Test")
        test_dependencies = [
            kos_safe_src.output,
            src_dir.joinpath("packages", "NUnit.2.6.4",
                             "lib", "nunit.framework.dll"),
            src_dir.joinpath("packages", "NSubstitute.1.9.2.0",
                             "lib", "net35", "NSubstitute.dll")
        ]
        test_src = src_dir.sub_dir("kOS.Safe.Test")
        test_target = test_src.ensure_dir("bin")
        test_src.output = test_target.joinpath("kOS.Safe.Test.dll")
        test_src.std_compile(references=test_dependencies)
        for test_dependency in test_dependencies:
            shutil.copy(test_dependency, test_target)

        logging.info("  Run tests")
        src_dir.run("mono", "--runtime=3.5",
                    "./packages/NUnit.Runners.2.6.4/tools/nunit-console.exe", test_src.output)

    def can_install(self):
         bin_target = self.project_dir.joinpath("Resources", "GameData", "kOS", "Plugins")
         return bin_target.joinpath("kOS.Safe.dll").exists() and  bin_target.joinpath("kOS.dll").exists()
         
    def install(self):
        target_dir = self.game_dir.joinpath("GameData", "kOS")
        rm_rf(target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "Resources", "GameData", "kOS"), target_dir)

    def check_installed(self):
        target_dir = self.game_dir.joinpath("GameData", "kOS")
        return target_dir.exists()
