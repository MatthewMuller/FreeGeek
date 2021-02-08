import os
import subprocess
import re

def get_drive_list():
    """
    This function gets attached drives from the OS and returns them as a list 
    """

    # get device list
    devices = system_call_with_output('ls /dev').split('\n')

    #remove any devices that are not drives (sarts with sd and doesn't end with a number) and return the list
    regex = re.compile(r"^sd.*[^[0-9]]*$")
    return [i for i in devices if regex.match(i)]

def drive_list_to_string(drive_list):

    #print drive list as comma separated list
    return (','.join(drive_list))


def system_call_with_output(cmd):

    return subprocess.getoutput(cmd)

def system_call_no_output(cmd):

    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return