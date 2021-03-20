import sys
import os
from fg_drive_lib import *


def main():

    drive_to_image = str(sys.argv[1])

    #print hard drive info before starting imaging script
    print_drive_info(drive_to_image)

    

if __name__ == "__main__":
    main()