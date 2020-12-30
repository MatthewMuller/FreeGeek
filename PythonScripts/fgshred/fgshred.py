
import time
import subprocess
import signal
from datetime import datetime
from fgshred_lib import *

parent_working_directory = ""

def main():


    protected_drives_list = []
    currently_attached_drives_list = []
    currently_wiping_drives_list = []
    shred_mode_enabled = False
    global parent_working_directory

    parent_working_directory = system_call_with_output('pwd').strip('\n')

    #register SIGINT for quitting script
    signal.signal(signal.SIGINT, signal_handler)

    #enter safe mode before starting main loop
    enter_safe_mode()
    protected_drives_list = get_drive_list()
    print_startup_info()
    print("    Protected drive list: " + drive_list_to_string(protected_drives_list) + "\n")

    #this will run until the user breaks the script
    while True:

        while not shred_mode_enabled:

            response = input("CAUTION: Enter shred mode? Type YES: ")
            print(str(response))
            if str(response) == 'EXIT' or str(response) == 'exit':
                exit()
            elif str(response) == 'YES' or str(response) == 'yes':
                #user has agreed to enter shred mode
                enter_shred_mode()
                shred_mode_enabled = True
            else:
                print("Sorry, I didnt understand. If you dont want to exit the program, type EXIT\n")


        counter = time.time()
        while shred_mode_enabled:

            #get currently attached drives
            currently_attached_drives_list = get_drive_list()

            #sort both drive lists
            protected_drives_list.sort()
            currently_attached_drives_list.sort()

            #for drives not in protected drive list
            for drive in list(set(currently_attached_drives_list) - set(protected_drives_list)):
            
                #if a new drive is detected
                if drive not in currently_wiping_drives_list:
                    
                    #start wiping drive
                    print("Starting wipe script for " + str(drive))
                    command = 'gnome-terminal -- python3 ' + parent_working_directory + '/shred_drive.py ' + str(drive)
                    os.system(str(command))
                    
                    #add drive to currently wiping drives
                    currently_wiping_drives_list.append(str(drive))

            #if wiping drive is disconnected
            for drive in currently_wiping_drives_list:
                if drive not in currently_attached_drives_list:
                    print("Drive " + str(drive) + " no longer connected.")
                    currently_wiping_drives_list.remove(str(drive))

            #give that CPU a break! :)
            time.sleep(5)

            # if 5 minutes have passed, print currently wiping drives 
            # to console with timestamp and reset counter
            if time.time() - counter > 300:
                counter = time.time()
                now = datetime.now()
                print(now.strftime("%d/%m/%Y %H:%M:%S") + " Drives currently being wiped: " + drive_list_to_string(currently_wiping_drives_list))

def signal_handler(sig, frame):
    print("\n") #for formatting
    enter_safe_mode()
    print('''         
Currently wiping drives will continue to wipe. You will
need to restart this script in order to enter shred mode again. Remember to
let currently shredding hard drives finish before restarting script.''')
    exit(0)


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
    
if __name__ == "__main__":
    main()