import sys
import os
import time
import signal

from FGDrive import *
from FGUtil import *


def main():
    """
    This script will print hard drive info and shred the drive.
    """

    # register SIGINT for quitting script
    signal.signal(signal.SIGINT, signal_handler)

    drive_to_shred = FGDrive(str(sys.argv[1]))

    # print hard drive info before starting shred
    drive_to_shred.print_short_drive_info()
    drive_to_shred.print_hd_health()

    print('\IMPORTANT: If errors are over threshold, close script and spike the drive')

    # promt user one last time that they for sure want to shred the drive
    response = str(input("Are you POSITIVE you want to shred drive " + drive_to_shred.get_device_name() + "? Type YES to proceed: "))
    
    # Only continue if user typed yes
    if response.lower() != "yes":
        print('''
You didnt type YES. Aborting shredding.
Unplug and reconnect drive to restart shredding process''')
        end_script()

    # delete all partions on connected drive
    print("Wiping all partions")
    drive_to_shred.wipe_partitions()

    # Shred the drive contents (3 passes)
    print("Destroying data now")
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