import os
import subprocess
import re

def init_fgshred():

    global parent_working_directory

    print_startup_info()
    parent_working_directory = system_call_with_output('pwd').strip('\n')

def get_drive_list():
    """
    This function gets attached drives from the OS and returns them as a list 
    """

    # get device list
    devices = system_call_with_output('ls /dev').split('\n')

    #remove any devices that are not drives (denoted by sd) and return the list
    regex = re.compile(r"^sd")
    return [i for i in devices if regex.match(i)]

def drive_list_to_string(drive_list):

    #print drive list as comma separated list
    return (','.join(drive_list) + "\n")

def enter_safe_mode():
    """
    Put code to be ran when entering safe mode here
    """

    print('Entering safe mode\n')
    
    #change background to safe mode 
    system_call_no_output("gsettings set org.gnome.desktop.background picture-uri file://" + str(parent_working_directory) + "/assets/safe_mode.png")

def enter_shred_mode():
    """
    Put code to be ran when entering shred mode here
    """

    print('''
********************
      BE AWARE
********************
Entering shred mode

Any drives attached to the system will now begin automatically being 
data shredding! Be aware...very aware! \n''')

    #change background to safe mode 
    system_call_no_output("gsettings set org.gnome.desktop.background picture-uri file://" + str(parent_working_directory) + "/assets/shred_mode.png")


def print_startup_info():

    print('''
    Welcome to the Free Geek Shred Program! :)

    This program is used to delete data on hard drives. It begins in safe mode,
    which will protect any drives attached (internal or external) from being
    shredded.

    Switching from safe mode to shred mode will enable hard drive shredding.
    This program will automatically begin shredding any newly detected drives 
    while in shred mode. This mean if you attach a hard drive while in shred mode,
    data on that drive will automatically be DESTROYED.

    NOTE: All protected drives should be connected for a minimum of a minute
    before starting this script. Verify the protected device list looks 
    correct before entering shred mode\n''')

def system_call_with_output(cmd):

    return subprocess.getoutput(cmd)

def system_call_no_output(cmd):

    proc=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, )
    return