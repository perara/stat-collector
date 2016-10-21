import os
import subprocess
import time

PATH = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = PATH + "/scripts/"

def execute(script_file, host, params=[]):
    script = os.path.join(SCRIPT_PATH, script_file)
    command = [
        '/bin/bash',
        os.path.join(PATH, "executor.sh"),
        host["port"],
        host["username"],
        host["address"],
        script
    ]
    command.extend(params)

    output = subprocess.check_output(command)
    return output