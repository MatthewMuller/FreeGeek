import time
import os
from datetime import datetime

from FGDriveList import *
from FGUtil import *

class FGShred:

    def __init__(self, pwd):
        self.mode = "safe"
        self.fg_drivelist = FGDriveList(pwd)

    def print_startup_info(self):
        """
        This function prints information about the Free Geek
        Shred Program on startup.
        """

        print('''
        Welcome to FG Shred! :)

        This program is used to delete data on hard drives. It begins in safe mode,
        which will protect any drives ALREADY attached (internal or external) from 
        being shredded.

        Switching from safe mode to shred mode will enable hard drive shredding.
        This program will automatically begin shredding any newly detected drives 
        while in shred mode. This mean if you attach a hard drive while in shred mode,
        data on that drive will automatically be DESTROYED.

        NOTE: All protected drives should be connected for a minimum of a minute
        before starting this script. Verify the protected device list looks 
        correct before entering shred mode\n''')

    def safe_mode(self):
        """
        This function is to be called when the Free Geek Shred
        Script is entering safe mode. It will change the desktop
        to the Safe Mode background and return.
        """

        print('Entering safe mode\n')

        self.mode = "safe"
        parent_working_directory = system_call_with_output('pwd').strip('\n')
        
        #change background to safe mode 
        system_call_no_output("gsettings set org.gnome.desktop.background picture-uri file://" + str(parent_working_directory) + "/assets/safe_mode.png")

    def shred_mode(self):
        """
        This function is to be called when the Free Geek Shred
        Script is entering shred mode. It will print a warning
        to console and change the desktop to the Shred Mode 
        background and return.
        """

        print('''
    ********************
        BE AWARE...!
    ********************

    Entering shred mode

    Any drives attached to the system will now begin automatically 
    shreddingdata! Be aware...be very aware! \n''')

        self.mode = "shred"
        parent_working_directory = system_call_with_output('pwd').strip('\n')

        #change background to shred mode 
        system_call_no_output("gsettings set org.gnome.desktop.background picture-uri file://" + str(parent_working_directory) + "/assets/shred_mode.png")

    def run(self):
        """
        Main daemon for FGShred. This function is a while 
        loop that runs continuously, which looks for newly 
        attached drives to wipe. When found, it wipes all 
        partitions on that drive and launches the 
        shred_drive.py script for that drive.
        """
        
        # print startup info
        self.print_startup_info()

        # enter safe mode before starting main loop
        self.safe_mode()
        print("\tProtected drive list: " + self.fg_drivelist.drive_list_to_string(self.fg_drivelist.get_protected_drive_list()) + "\n")

        # this will run until the user breaks the script
        while True:

            # safe mode
            while self.mode == "safe":

                response = input("CAUTION: Enter shred mode? Type YES: ")
                print(str(response))
                if str(response).lower() == 'exit':
                    exit()
                elif str(response).lower() == 'yes':
                    # user has agreed to enter shred mode
                    self.shred_mode()
                else:
                    print("Sorry, I didnt understand. If you want to exit the program, type EXIT\n")

            # Set counter before starting next loop
            counter = time.time()

            #shred mode
            while self.mode == "shred":

                # Update the connected drive list
                self.fg_drivelist.update_connected_drive_list()

                # for drives not in protected drive list
                for drive in self.fg_drivelist.get_not_protected_drive_list():
                    
                    # if a new drive is detected
                    if drive not in self.fg_drivelist.get_in_progress_list():

                        print("Processing drive " + drive.get_device_name())

                        # call shred script on drive
                        print("\tStarting wipe script")
                        command = 'gnome-terminal -- python3 ' + self.fg_drivelist.get_pwd() + '/ShredDrive.py ' + drive.get_device_name()
                        os.system(str(command))
                        
                        # add drive to currently wiping drives
                        self.fg_drivelist.add_in_progress_drive(drive)

                # Check for disconnected drives
                for drive in self.fg_drivelist.get_in_progress_list():
                    if drive not in self.fg_drivelist.get_connected_drive_list():
                        print("Drive " + drive.get_device_name() + " no longer connected.")
                        self.fg_drivelist.remove_in_progress_drive(drive.get_device_name())

                #give that CPU a break! :)
                time.sleep(5)

                # if 30 seconds have passed, print currently wiping drives 
                # to console with timestamp and reset counter
                if time.time() - counter > 30:
                    counter = time.time()
                    now = datetime.now()
                    print(now.strftime("%d/%m/%Y %H:%M:%S") + " Drives currently being wiped: " + str(self.fg_drivelist.drive_list_to_string(self.fg_drivelist.get_in_progress_list())))