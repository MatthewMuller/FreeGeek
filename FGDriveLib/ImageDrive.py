import sys
import os
import time
import signal

import FGDrive
from FGUtil import *


def main():
    """
    This script will print hard drive info and shred the drive.
    """

    # register SIGINT for quitting script
    signal.signal(signal.SIGINT, signal_handler)

    # argv1 is drive name (ex. sdc)
    drive_to_shred = FGDrive(str(sys.argv[1]))

    # print hard drive info before starting shred
    drive_to_shred.print_short_drive_info()
    drive_to_shred.print_hd_health()

    print('\IMPORTANT: If errors are over threshold, close script and spike the drive')

    # promt user one last time that they for sure want to shred the drive
    response = str(input("Are you POSITIVE you want to image drive " + drive_to_shred.get_device_name() + "? Type YES to proceed: "))
    
    # Only continue if user typed yes
    if response.lower() != "yes":
        print('''
You didnt type YES. Aborting imaging.
Unplug and reconnect drive to restart imaging process''')
        end_script()

    # delete all partions on connected drive
    print("Wiping all partions")
    drive_to_shred.wipe_partitions()

    # display available images:
    # TODO: Make this a menu
    for filename in os.listdir(str(os.getcwd()) + "/Images"):
        answer = input("Image " + str(filename) +" ? Type YES")


    # Shred the drive contents (3 passes)
    print("imaging drive now")
    os.system('sudo shred -vf -n 2 /dev/' + drive_to_shred.get_device_name())

    #print hard drive info one last time
    drive_to_shred.print_short_drive_info()
    drive_to_shred.print_hd_health()

    end_script()

def end_script():
    # keep window open so user can read output. They can close
    # the terminal to close the script 
    while(True):
        time.sleep(5)

def signal_handler(sig, frame):
    print('''\n
Stopping shred script. If drive was not done shredding, 
reconnect drive and shred again. You can safely close this window''')
    exit(0)

if __name__ == "__main__":
    main()