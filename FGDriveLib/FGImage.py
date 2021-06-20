import time
import os
from datetime import datetime

import FGDriveList
from FGUtil import *

class FGImage:

    def __init__(self, pwd):
        self.fg_drivelist = FGDriveList(pwd)

    def print_startup_info(self):
        """
        This function prints information about the Free Geek
        Image Program on startup.
        """

        print('''
        Welcome to FG Image! :)

        This program is used to image hard drives.\n''')

    def safe_mode(self):
        """
        This function is to be called when the Free Geek Image
        Program is entering safe mode. It will change the desktop
        to the Safe Mode background and return.
        """

        print('Entering safe mode\n')

        self.mode = "safe"
        parent_working_directory = system_call_with_output('pwd').strip('\n')
        
        #change background to safe mode 
        system_call_no_output("gsettings set org.gnome.desktop.background picture-uri file://" + str(parent_working_directory) + "/assets/safe_mode.png")

    def image_mode(self):
        """
        This function is to be called when the Free Geek Image
        Program is entering image mode. It will print a warning
        to console and change the desktop to the image Mode 
        background and return.
        """

        print('''
    ********************
        BE AWARE...!
    ********************

    Entering iage mode

    Any drives attached to the system will now begin automatically be 
    imaged! Be aware...be very aware! \n''')

        self.mode = "image"
        parent_working_directory = system_call_with_output('pwd').strip('\n')

        #change background to shred mode 
        system_call_no_output("gsettings set org.gnome.desktop.background picture-uri file://" + str(parent_working_directory) + "/assets/image_mode.png")

    def run(self):
        """
        Main daemon for FGImage. This function is a while 
        loop that runs continuously, which looks for newly 
        attached drives to image. When found, it launces the
        image_drive.py script for that drive.
        """

        # enter safe mode before starting main loop
        self.safe_mode()
        print("\tProtected drive list: " + self.fg_drivelist.drive_list_to_string(self.fg_drivelist.get_protected_drive_list()) + "\n")

        # this will run until the user breaks the script
        while True:

            # safe mode
            while self.mode == "safe":

                response = input("CAUTION: Enter image mode? Type YES: ")
                print(str(response))
                if str(response).lower() == 'exit':
                    exit()
                elif str(response).lower() == 'yes':
                    # user has agreed to enter shred mode
                    self.image_mode()
                else:
                    print("Sorry, I didnt understand. If you want to exit the program, type EXIT\n")

            # Set counter before starting next loop
            counter = time.time()

            #shred mode
            while self.mode == "image":

                # Update the connected drive list
                self.fg_drivelist.update_connected_drive_list()

                # for drives not in protected drive list
                for drive in list(set(self.fg_drivelist.get_connected_drive_list()) - set(self.fg_drivelist.get_protected_drive_list())):
                
                    # if a new drive is detected
                    if drive not in self.fg_drivelist.get_in_progress_list():

                        print("Processing drive " + str(drive))

                        # call image script on drive
                        print("\tStarting image script")
                        command = 'gnome-terminal -- python3 ' + self.fg_drivelist.get_pwd() + '/ImageDrive.py ' + str(drive)
                        os.system(str(command))
                        
                        # add drive to currently wiping drives
                        self.fg_drivelist.add_in_progress_drive(str(drive))

                # Check for disconnected drives
                for drive in self.fg_drivelist.get_in_progress_list():
                    if drive not in self.fg_drivelist.get_connected_drive_list():
                        print("Drive " + str(drive) + " no longer connected.")
                        self.fg_drivelist.remove_in_progress_drive(str(drive))

                #give that CPU a break! :)
                time.sleep(5)

                # if 30 seconds have passed, print currently wiping drives 
                # to console with timestamp and reset counter
                if time.time() - counter > 30:
                    counter = time.time()
                    now = datetime.now()
                    print(now.strftime("%d/%m/%Y %H:%M:%S") + " Drives currently being image: " + str(self.fg_drivelist.drive_list_to_string(self.fg_drivelist.get_in_progress_list)))