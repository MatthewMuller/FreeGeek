from FGDrive import *

class FGShred:

    def __init__(self, pwd):
        self.mode = "safe"
        self.FGdrive = FGDrive(pwd)

       __print_startup_info__()

    def __print_startup_info():
        """
        This function prints information about the Free Geek
        Shred Script on startup.
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

    def __safe_mode():
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

    def __shred_mode():
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

    Any drives attached to the system will now begin automatically being 
    data shredding! Be aware...be very aware! \n''')

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

        # enter safe mode before starting main loop
        self.safe_mode()
        print("\tProtected drive list: " + self.FGDrive.drive_list_to_string() + "\n")

        # this will run until the user breaks the script
        while True:

            # safe mode
            while mode == "safe":

                response = input("CAUTION: Enter shred mode? Type YES: ")
                print(str(response))
                if str(response) == 'EXIT' or str(response) == 'exit':
                    exit()
                elif str(response) == 'YES' or str(response) == 'yes':
                    # user has agreed to enter shred mode
                    self.shred_mode()
                else:
                    print("Sorry, I didnt understand. If you dont want to exit the program, type EXIT\n")

            counter = time.time()

            #shred mode
            while mode == "shred":

                # Update the connected drive list
                update_connected_drive_list():

                # for drives not in protected drive list
                for drive in list(set(self.FGDrive.get_connected_drive_list()) - set(self.FGDrive.get_protected_drive_list())):
                
                    # if a new drive is detected
                    if drive not in self.FGDrive.get_wiping_drive_list():

                        print("Processing drive " + str(drive))

                        # delete all partions on connected drive
                        print("\tWiping all partions")
                        syscall_output = system_call_with_output("sudo dd if=/dev/zero of=/dev/"+ str(drive) + " bs=512 count=1 conv=notrunc").split("\n")
                        for line in syscall_output:
                            print("\t\t" + str(line))

                        # call shred script on drive
                        print("\tStarting wipe script")
                        command = 'gnome-terminal -- python3 ' + parent_working_directory + '/shred_drive.py ' + str(drive)
                        os.system(str(command))
                        
                        # add drive to currently wiping drives
                        self.FGDrive.add_wiping_drive(str(drive))

                # Check for disconnected drives
                for drive in self.FGShred.get_wiping_drive_list():
                    if drive not in self.FGDrive.get_connected_drive_list():
                        print("Drive " + str(drive) + " no longer connected.")
                        self.FGDrive.remove_wiping_drive(str(drive))

                #give that CPU a break! :)
                time.sleep(5)

                # if 30 seconds have passed, print currently wiping drives 
                # to console with timestamp and reset counter
                if time.time() - counter > 30:
                    counter = time.time()
                    now = datetime.now()
                    print(now.strftime("%d/%m/%Y %H:%M:%S") + " Drives currently being wiped: " + drive_list_to_string(currently_wiping_drives_list))