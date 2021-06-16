from FGUtil import *

class FGDrive:

    def __init__(self, drive_device_name):
        self.drive_device_name = str(drive_device_name)

    def get_device_name(self):
        return self.drive_device_name

    def print_short_drive_info(self):
        print(system_call_with_output("sudo smartctl -i /dev/" + self.drive_device_name))

    def print_long_drive_info(self):
        print(system_call_with_output("sudo smartctl -a /dev/" + self.drive_device_name))

    def wipe_partitions(self, drive):
        syscall_output = system_call_with_output("sudo dd if=/dev/zero of=/dev/" + self.drive_device_name + " bs=512 count=1").split("\n")
        for line in syscall_output:
            print("\t\t" + str(line))

    def print_hd_health(self,drive):
        print("/n HD Health")
        print(system_call_with_output("sudo smartctl -i /dev/" + self.drive_device_name + " | grep -i 'ID# ATTRIBUTE \|Raw_Read \|Reallocated\|Seek_Error_Rate\|Spin_Up_Time\|Power_On_Hours'"))