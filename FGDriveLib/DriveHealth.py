import signal

def main():
    """
    This script will print hard drive health info.
    """

    # register SIGINT for quitting script
    signal.signal(signal.SIGINT, signal_handler)

    # argv1 is drive name (ex. sdc)
    drive_to_health_check = FGDrive(str(sys.argv[1]))

    # print hard drive info before starting shred
    drive_to_health_check.print_short_drive_info()
    drive_to_health_check.print_hd_health()

    end_script()

def end_script():
    # keep window open so user can read output. They can close
    # the terminal to close the script 
    while(True):
        time.sleep(5)

def signal_handler(sig, frame):
    print('''\n
Stopping shred script. If drive was not done shredding, 
reconnect drive and shred again. You can safely close this window''')
    exit(0)

if __name__ == "__main__":
    main()