
import time
from datetime import datetime
from fgshred_lib import *

parent_working_directory = ""

def main():


    protected_drives_list = []
    currently_attached_drives_list = []
    currently_wiping_drives_list = []
    shred_mode_enabled = False

    #initialize the fgshred library
    init_fgshred()

    #enter safe mode before starting main loop
    enter_safe_mode()
    protected_drives_list = get_drive_list()
    print("    Protected drive list: " + drive_list_to_string(protected_drives_list))

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
            
                if drive not in currently_wiping_drives_list:
                    #start wiping drive
                    print("Starting wipe script for " + str(drive))


                    #add drive to currently wiping drives
                    currently_wiping_drives_list.append(str(drive))

            #give that CPU a break! :)
            time.sleep(5)

            # if 5 minutes have passed, print currently wiping drives 
            # to console with timestamp and reset counter
            if time.time() - counter > 10:
                counter = time.time()
                now = datetime.now()
                print(now.strftime("%d/%m/%Y %H:%M:%S") + " Drives currently being wiped: " + drive_list_to_string(currently_wiping_drives_list))
main()