import sys
import os
from fg_drive_lib import system_call_with_output


def main():
    """
    This script does three things:
        Calls shred on the passed in drive
        Runs SMART control tests on the drive
        Prints drive information to console
    """

    drive_to_shred = str(sys.argv[1])

    #print hard drive info before starting shred
    print(system_call_with_output("sudo smartctl -i /dev/" + str(drive_to_shred)))

    #promt user one last time that they for sure want to shred the drive
    response = input("Are you POSITIVE you want to shred drive " + drive_to_shred + "? Type YES to proceed: ")
    if response == "YES" or response == 'yes':
        os.system('sudo shred -vf -n 3 /dev/' + drive_to_shred)

        #print hard drive info after starting shred
        print("\n\n" + system_call_with_output("sudo smartctl -i /dev/" + str(drive_to_shred)))
    else:
        print('''
You didnt type YES. Aborting shredding.
Unplug and reconnect drive to restart shredding process"''')

    while(True):
        #keep window open so user can read output. They can close
        #the terminal to close the script
        pass

if __name__ == "__main__":
    main()