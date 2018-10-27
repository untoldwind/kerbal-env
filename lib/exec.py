import subprocess
import logging
from lib.utils import mkdir_p


def run_command(cwd, command, env=None):
    logging.debug("Exec command in '%s': %s" % (cwd, command))
    result = subprocess.run(command, cwd=cwd, capture_output=True, env=env)
    logging.debug("Exit code: %d" % (result.returncode))
    if result.returncode != 0:
        logging.error("Command %s failed" % (command))
        logging.error("Out:")
        logging.error(result.stdout.decode('utf-8'))
        logging.error("Err:")
        logging.error(result.stderr.decode('utf-8'))
        raise NameError("Command %s failed" % (command))
    else:
        logging.debug("Out:")
        logging.debug(result.stdout.decode('utf-8'))
        logging.debug("Err:")
        logging.debug(result.stderr.decode('utf-8'))


class SourceDir:
    def __init__(self, game_dir, path):
        self._game_dir = game_dir
        self._path = path
        self._resources = []
        self._output = None

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value):
        self._output = value

    @property
    def path(self):
        return self._path

    def sub_dir(self, *args):
        return SourceDir(self._game_dir, self.path.joinpath(*args))

    def ensure_dir(self, *args):
        path = self.path.joinpath(*args)
        mkdir_p(path)
        return path

    def joinpath(self, *args):
        return self.path.joinpath(*args)

    def nuget_restore(self):
        logging.info("  nuget restore")
        run_command(cwd=self.path,  command=["nuget", "restore"])

    def nuget_install(self, name, version):
        logging.info("  nuget install: %s" % name)
        run_command(cwd=self.path,  command=[
                    "nuget", "install", name, "-Version", version])

    def resgen(self, src, dest, references=[], lib_paths=[]):
        logging.info("   Resgen")
        run_command(cwd=self.path, command=["resgen", "/useSourcePath", "/compile", "%s,%s" % (src, dest)] +
                    ["/lib:%s" % lib for lib in lib_paths] +
                    ["/reference:%s" % reference for reference in references])
        self._resources.append(dest)

    def compile_all(self, output, recurse = "*.cs", resources=[], references=[], lib_paths=[], extra_args=[]):
        logging.info("   Compile C#")
        command = ["csc", "/target:library", "/utf8output", "/platform:AnyCPU",
                   "/noconfig", "/nowarn:1701,1702", "/nostdlib+", "/errorreport:prompt",
                   "/warn:4", "/debug-", "/filealign:512", "/optimize+", "/highentropyva-",
                   "/out:%s" % output, "/recurse:%s" % recurse] + extra_args + ["/resource:%s" % resource for resource in resources]
        if len(lib_paths) > 0:
            command.append("/lib:%s" %
                           ",".join([str(lib) for lib in lib_paths]))
        if len(references) > 0:
            command.append("/reference:%s" %
                           ",".join([str(reference) for reference in references]))
        run_command(cwd=self.path, command=command)

    def std_compile(self, references=[], extra_args=[]):
        std_libs = ["System.dll", "System.Core.dll", "System.Xml.dll", "mscorlib.dll"]
        self.compile_all(output=self._output, recurse="*.cs", lib_paths=["%s/KSP_Data/Managed" % self._game_dir], resources=self._resources,
                         references=["%s/KSP_Data/Managed/%s" % (self._game_dir, lib) for lib in std_libs] + references, extra_args=extra_args)

    def run(self, *args):
        run_command(cwd=self.path, command=args)
