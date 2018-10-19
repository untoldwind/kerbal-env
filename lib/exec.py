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
