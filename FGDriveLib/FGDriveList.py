import re

from FGDrive import *
from FGUtil import *

class FGDriveList:

    in_progress_list = []
    protected_list = []
    connected_drive_list = []

    def __init__(self, pwd):

        self.protected_list = self.get_attached_drive_list().copy()
        self.protected_list.sort(key=lambda FGDrive: FGDrive.drive_device_name)
        self.connected_drive_list = self.get_attached_drive_list().copy()
        self.connected_drive_list.sort(key=lambda FGDrive: FGDrive.drive_device_name)
        self.pwd = pwd


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
    
    def get_protected_drive_list_device_names(self):
        return list(drive.drive_device_name for drive in self.get_protected_drive_list())

    def get_connected_drive_list(self):
        return self.connected_drive_list

    def get_not_protected_drive_list(self):
        return list(filter(lambda drive: drive.get_device_name() not in self.get_protected_drive_list_device_names(), self.get_connected_drive_list()))

    def get_connected_drive_list_device_names(self):
        return list(drive.drive_device_name for drive in self.get_connected_drive_list())

    def update_connected_drive_list(self):
        self.connected_drive_list = self.get_attached_drive_list().copy()
        self.connected_drive_list.sort(key=lambda FGDrive: FGDrive.drive_device_name)

    def get_in_progress_list(self):
        return self.in_progress_list

    def add_in_progress_drive(self, drive):
        self.in_progress_list.append(drive)
    
    def remove_in_progress_drive(self, drive):
        self.in_progress_list.remove(drive)

    def drive_list_to_string(self, drive_list):
        drive_list_string = ""
        for drive in drive_list:
            drive_list_string = drive_list_string + drive.get_device_name()
        
        return drive_list_string
