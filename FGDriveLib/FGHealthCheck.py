import FGDriveList
from FGUtil import *

class FGHealthCheck:

    def __init__(self, pwd):
        self.fg_drivelist = FGDriveList(pwd)

    def print_startup_info(self):
        """
        This function prints information about the Free Geek
        Health Check Program on startup.
        """

        print('''
        Welcome to FG Hard Drive Health Check! :)

        This program is used to check the health of hard drives. On startup,
        any currently attached drive will be excluded from health check.

        Once started, any newly attached hard drive will have its health
        information printed to a new window.

        NOTE: All currently attached drives should be connected for a minimum 
        of a minute before starting this script\n''')

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
        print("\Currently connected drives: " + self.fg_drivelist.drive_list_to_string(self.fg_drivelist.get_protected_drive_list()) + "\n")

        # this will run until the user breaks the script
        while True:

            # Update the connected drive list
                self.fg_drivelist.update_connected_drive_list()

                # for drives not in protected drive list
                for drive in list(set(self.fg_drivelist.get_connected_drive_list()) - set(self.fg_drivelist.get_protected_drive_list())):
                
                    # if a new drive is detected
                    if drive not in self.fg_drivelist.get_in_progress_list():

                        # print health
                        print("Printing drive health for " + str(drive))
                        command = 'gnome-terminal -- python3 ' + self.fg_drivelist.get_pwd() + '/DriveHealth.py ' + str(drive)
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