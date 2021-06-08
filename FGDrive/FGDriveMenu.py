import time
import os
import signal

from FGShred import *

def main():

    # register SIGINT for quitting script
    signal.signal(signal.SIGINT, signal_handler)

    # clear terminal
    os.system("clear")

    while (True):

        menu_item = input('''
********************************************
Welcome to FG Drive! What do you want to do?

1: Shred Drives
2: Image Drives
3: Check Drive Health
********************************************\n''')
    
         # Shred
        if('1' == str(menu_item) ):
            fg_shred = FGShred(os. getcwd())
            #os.system("clear")
            fg_shred.run()
        # Image
        elif('2' == menu_item):

            print("Not Implemented")
        # Drive Health
        elif('3' == menu_item):
            print("Not Implemented")
        else:
            print("Yikes! Bad input!")
            time.sleep(2)
            os.system("clear")

def signal_handler(sig, frame):
    print('''\n         
Currently wiping drives will continue to wipe. You will
need to restart this script in order to enter shred mode again. Remember to
let currently shredding hard drives finish before restarting script.''')
    exit(0)

if __name__ == "__main__":
    main()