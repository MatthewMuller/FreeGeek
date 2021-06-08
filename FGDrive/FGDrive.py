import re

from FGUtil import *

class FGDrive:

    wiping_list = []
    protected_list = []
    connected_drive_list = []
    imaging_list = []

    def __init__(self, pwd):

        self.protected_list = self.get_drive_list().copy()
        self.protected_list.sort()
        self.connected_drive_list = self.get_drive_list().copy()
        self.connected_drive_list.sort()
        self.pwd = str(pwd)

    def get_drive_list(self):
        """
        This function gets attached drives from the OS and returns them as a list 
        """

        # get device list
        devices = system_call_with_output('ls /dev').split('\n')

        #remove any devices that are not drives (sarts with sd and doesn't end with a number) and return the list
        regex = re.compile(r"^sd.*[^[0-9]]*$")
        return [i for i in devices if regex.match(i)]

    def get_protected_drive_list(self):
        return self.protected_list

    def get_connected_drive_list(self):
        return self.connected_drive_list

    def update_connected_drive_list(self):
        self.connected_drive_list = self.get_drive_list().copy()
        self.connected_drive_list.sort()

    def get_pwd(self):
        return self.pwd

    def get_wiping_drive_list(self):
        return self.wiping_list

    def add_wiping_drive(self, drive):
        self.wiping_list.append(str(drive))
    
    def remove_wiping_drive(self, drive):
        self.wiping_list.remove(str(drive))

    def drive_list_to_string(self, drive_list):
        return ','.join(drive_list)

    def print_short_drive_info(self, drive):
        print(system_call_with_output("sudo smartctl -i /dev/" + str(drive)))

    def print_long_drive_info(self, drive):
        print(system_call_with_output("sudo smartctl -a /dev/" + str(drive)))

    def wipe_partitions(self, drive):
        syscall_output = system_call_with_output("sudo dd if=/dev/zero of=/dev/"+ str(drive) + " bs=512 count=1 conv=notrunc").split("\n")
        for line in syscall_output:
            print("\t\t" + str(line))
