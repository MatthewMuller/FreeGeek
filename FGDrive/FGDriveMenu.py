from FGShred import *
import time
import os

def print_menu():

     print('''
********************************************
Welcome to FG Drive! What do you want to do?

1: Shred Drives
2: Image Drives
3: Check Drive Health
********************************************
    '''))

def main():

    #register SIGINT for quitting script
    signal.signal(signal.SIGINT, signal_handler)

    while (True):

        menu_item = input(print_menu())
    
         # Shred
        if(menu_item == "1"):
            fg_shred = FGShred(os. getcwd())
            os.system("clear")
            fg_shred.run()
        # Image
        elif(menu_item == "2"):

            print("Not Implemented")
        # Drive Health
        elif(menu_item == "3"):
            print("Not Implemented")
        else:
            print("Yikes! Bad input!")
            time.sleep(2)
            os.system("clear")

def signal_handler(sig, frame):
    """
    This function catches a Ctrl + C keypress and prints out
    information about the Free Geek Shred Script closing.
    """

    print("\n") #for formatting
    enter_safe_mode()
    print('''         
Currently wiping drives will continue to wipe. You will
need to restart this script in order to enter shred mode again. Remember to
let currently shredding hard drives finish before restarting script.''')
    exit(0)

if __name__ == "__main__":
    main()