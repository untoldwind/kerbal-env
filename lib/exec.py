import subprocess

def run_command(pwd, command, debug):
    if debug:
        print("Exec command in '%s': %s" % (pwd, command))
    result = subprocess.run(command, cwd = pwd, capture_output=True)
    if debug:
        print("Exit code: %d" % (result.returncode))
    if result.returncode != 0:
        print("Command %s failed" % (command))
        print("Out:")
        print(result.stdout.decode('utf-8'))
        print("Err:")
        print(result.stderr.decode('utf-8'))
        raise NameError("Command %s failed" % (command))