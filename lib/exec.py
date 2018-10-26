import subprocess
import logging


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


def resgen(cwd, src, dest, references=[], lib_paths=[]):
    logging.info("   Resgen")
    run_command(cwd=cwd, command=["resgen", "/useSourcePath", "/compile", "%s,%s" % (src, dest)] +
                ["/lib:%s" % lib for lib in lib_paths] +
                ["/reference:%s" % reference for reference in references])


def compile_all(cwd, output, recurse, resources=[], references=[], lib_paths=[]):
    logging.info("   Compile C#")
    command = ["csc", "/target:library", "/utf8output",
               "/noconfig", "/nowarn:1701,1702", "/nostdlib+", "/errorreport:prompt",
               "/warn:4", "/define:TRACE",
               "/debug:pdbonly", "/filealign:512", "/optimize+",
               "/highentropyva-",
               "/out:%s" % output, "/recurse:%s" % recurse] + ["/resource:%s" % resource for resource in resources]
    if len(lib_paths) > 0:
        command.append("/lib:%s" % ",".join([str(lib) for lib in lib_paths]))
    if len(references) > 0:
        command.append("/reference:%s" % ",".join([str(reference) for reference in references]))
    run_command(cwd=cwd, command=command)
