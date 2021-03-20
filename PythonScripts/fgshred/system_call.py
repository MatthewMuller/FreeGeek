import os
import subprocess

def system_call_with_output(cmd):
    """
    Calls subprocess and returns subprocess output
    """

    return subprocess.getoutput(cmd)

def system_call_no_output(cmd):
    """
    Calls subprocess and returns without subprocess output
    """

    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return
