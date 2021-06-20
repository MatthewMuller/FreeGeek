import sys
import os
import time
import signal

import FGDrive
from FGUtil import *


def main():
    """
    This script will print hard drive info and image the drive.
    """

    # register SIGINT for quitting script
    signal.signal(signal.SIGINT, signal_handler)

    # argv1 is drive name (ex. sdc)
    drive_to_image = FGDrive(str(sys.argv[1]))

    # print hard drive info before starting shred
    drive_to_image.print_short_drive_info()
    drive_to_image.print_hd_health()

    print('\IMPORTANT: If errors are over threshold, close script and spike the drive')

    # promt user one last time that they for sure want to shred the drive
    response = str(input("Are you POSITIVE you want to image drive " + drive_to_image.get_device_name() + "? Type YES to proceed: "))
    
    # Only continue if user typed yes
    if response.lower() != "yes":
        print('You didnt type YES. Aborting imaging. Unplug and reconnect drive to restart imaging process')
        end_script()

    # delete all partions on connected drive
    print("Wiping all partions")
    drive_to_image.wipe_partitions()

    # get list of images
    imagelist = os.listdir(str(os.getcwd()) + "/../Images")

    for menu_number, filename in enumerate(imagelist):
        print(str(int(menu_number) + 1) + ": " + str(filename))

    selected_menu_number = input("What would you like to image?\n")

    if(selected_menu_number <= 0 or selected_menu_number > len(imagelist)):
        print("Bad input. Unplug and reconnect drive to restart imaging process")
        end_script()

    # Image the drive
    print("imaging drive now")
    os.system('sudo qemu-img convert ' + str(imagelist[selected_menu_number - 1]) + ' -O raw ' + str(os.getcwd()) + "/../Images/" + str(drive_to_image.get_device_name()))

    # Expand primary partition TODO: Figure out what partitions to expand
    os.system("sudo resize2fs /dev/TODO" + str(drive_to_image.get_device_name()) + ' -d -f')
    os.system("sudo resize2fs /dev/TODO" + str(drive_to_image.get_device_name()) + ' -d -f')

    #print hard drive info one last time
    drive_to_image.print_short_drive_info()
    drive_to_image.print_hd_health()

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