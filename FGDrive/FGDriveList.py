import re

from FGUtil import *

class FGDriveList:

    wiping_list = []
    protected_list = []
    connected_drive_list = []
    imaging_list = []

    def __init__(self, pwd):

        self.protected_list = self.get_attached_drive_list().copy()
        self.protected_list.sort()
        self.connected_drive_list = self.get_attached_drive_list().copy()
        self.connected_drive_list.sort()
        self.pwd = str(pwd)

    def get_attached_drive_list(self):
        """
        This function gets attached drives from the OS and returns them as a list of FGDrives
        """

        # device list
        attached_drive_list = []

        # get device list
        devices = system_call_with_output('ls /dev').split('\n')

        # remove any devices that are not drives (sarts with sd and doesn't end with a number)
        regex = re.compile(r"^sd.*[^[0-9]]*$")
        filtered_device_list = [i for i in devices if regex.match(i)]

        # create a drive object for each attached drive
        for drive in filtered_device_list:
            attached_drive_list.append(FGDrive(drive))

        return attached_drive_list

    def get_pwd(self):
        return self.pwd

    def get_protected_drive_list(self):
        return self.protected_list

    def get_connected_drive_list(self):
        return self.connected_drive_list

    def update_connected_drive_list(self):
        self.connected_drive_list = self.get_attached_drive_list().copy()
        self.connected_drive_list.sort()

    def get_wiping_drive_list(self):
        return self.wiping_list

    def add_wiping_drive(self, drive):
        self.wiping_list.append(FGDrive(str(drive)))
    
    def remove_wiping_drive(self, drive):
        self.wiping_list.remove(FGDrivestr(drive))

    def drive_list_to_string(self, drive_list):
        return ','.join(drive_list)
