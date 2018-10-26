import logging
import shutil
from lib.exec import run_command, resgen, compile_all
from lib.utils import ln_s, rm_rf, mkdir_p, rm


def build(game_dir, project_dir):
    src_dir = project_dir.joinpath("src")
    bin_target = project_dir.joinpath(
        "Resources", "GameData", "kOS", "Plugins")
    logging.info("  nuget restore")
    run_command(cwd=src_dir,  command=["nuget", "restore"])
    run_command(cwd=src_dir.joinpath("packages"),  command=[
                "nuget", "install", "NUnit.Runners", "-Version", "2.6.4"])
    run_command(cwd=src_dir.joinpath("packages"),  command=[
                "nuget", "install", "SharpZipLib", "-Version", "0.86.0"])

    rm(bin_target, "*")
    shutil.copy(src_dir.joinpath("packages", "SharpZipLib.0.86.0",
                                 "lib", "20", "ICSharpCode.SharpZipLib.dll"), bin_target)

    logging.info("  Build kOS.Safe")
    mkdir_p(src_dir.joinpath("kOS.Safe", "obj"))
    resgen(cwd=src_dir.joinpath("kOS.Safe"), src="Properties/Resources.resx",
           dest="obj/kOS.Safe.Properties.Resources.resources")
    compile_all(cwd=src_dir.joinpath("kOS.Safe"), output=bin_target.joinpath("kOS.Safe.dll"), recurse="*.cs", resources=["obj/kOS.Safe.Properties.Resources.resources"],
                lib_paths=["%s/KSP_Data/Managed" % game_dir],
                references=["System.dll", "System.Core.dll", "System.Xml.dll", "mscorlib.dll", bin_target.joinpath("ICSharpCode.SharpZipLib.dll")])

    logging.info("  Build kOS")
    mkdir_p(src_dir.joinpath("kOS", "obj"))
    resgen(cwd=src_dir.joinpath("kOS"), src="Properties/Resources.resx",
           dest="obj/kOS.Properties.Resources.resources")
    compile_all(cwd=src_dir.joinpath("kOS"), output=bin_target.joinpath("kOS.dll"), recurse="*.cs", resources=["obj/kOS.Properties.Resources.resources"],
                lib_paths=[bin_target, "%s/KSP_Data/Managed" % game_dir],
                references=["System.dll", "System.Core.dll", "System.Xml.dll", "mscorlib.dll", "Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll", "kOS.Safe.dll"])

    logging.info("  Build kOS.Safe.Test")
    test_target = src_dir.joinpath("kOS.Safe.Test", "bin")
    mkdir_p(test_target)
    compile_all(cwd=src_dir.joinpath("kOS.Safe.Test"), output=test_target.joinpath("kOS.Safe.Test.dll"), recurse="*.cs",
                lib_paths=[bin_target, "%s/KSP_Data/Managed" % game_dir,
                           src_dir.joinpath("packages", "NSubstitute.1.9.2.0", "lib", "net35")],
                references=["System.dll", "System.Core.dll", "System.Xml.dll", "mscorlib.dll", "kOS.Safe.dll", src_dir.joinpath("packages", "NUnit.2.6.4", "lib", "nunit.framework.dll"), "NSubstitute.dll"])
    shutil.copy(src_dir.joinpath("packages", "NUnit.2.6.4",
                                 "lib", "nunit.framework.dll"), test_target)
    shutil.copy(src_dir.joinpath("packages", "NSubstitute.1.9.2.0",
                                 "lib", "net35", "NSubstitute.dll"), test_target)
    shutil.copy(bin_target.joinpath("kOS.Safe.dll"), test_target)
    shutil.copy(bin_target.joinpath("kOS.dll"), test_target)

    logging.info("  Run tests")
    run_command(cwd=src_dir, command=[
                "mono", "./packages/NUnit.Runners.2.6.4/tools/nunit-console.exe", test_target.joinpath("kOS.Safe.Test.dll")])


def install(game_dir, project_dir):
    target_dir = game_dir.joinpath("GameData", "kOS")
    rm_rf(target_dir)
    shutil.copytree(project_dir.joinpath(
        "Resources", "GameData", "kOS"), target_dir)


def check_installed(game_dir):
    target_dir = game_dir.joinpath("GameData", "kOS")
    return target_dir.exists()
