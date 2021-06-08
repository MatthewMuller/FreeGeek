class FGDrive:
    
    self.wiping_list
    self.imaging_list
    
    def __init__(self, pwd):
        self.pwd = pwd
        self.protected_list = get_drive_list().sort()
        self.connected_drive_list = get_drive_list().sort()

        __print_startup_info__()

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
        connected_drive_list = get_drive_list().sort()

    def get_pwd(self):
        return self.pwd

    def get_wiping_drive_list(self):
        return self.wiping_list

    def add_wiping_drive(self, drive):
        self.wiping_list.append(str(drive))
    
    def remove_wiping_drive(self, dive):
        self.wiping_list.remove(str(drive))

    def drive_list_to_string():
        #print drive list as comma separated list
        return (','.join(drive_list))

    def print_short_drive_info(self, drive):
        """
        Prints the drive's SMART information
        """

        print(system_call_with_output("sudo smartctl -i /dev/" + str(drive)))
        return

    def print_long_drive_info(self. drive):
        """
        Prints the drive's SMART information
        """

        print(system_call_with_output("sudo smartctl -a /dev/" + str(drive)))
        return
    
 
