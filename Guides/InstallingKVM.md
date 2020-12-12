# Installing KVM

This guide is written to install and setup KVM in Ubuntu 18.04. 

This relies HEAVILY on the guide found here: https://linuxconfig.org/install-and-set-up-kvm-on-ubuntu-18-04-bionic-beaver-linux


# Installing

Run the following to install the KVM program:

``` bash
sudo apt install qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager
```

# Add libvirt to Group

Run the following commands so we can grant libvert root privileges.

``` bash
sudo adduser <username> libvirt
sudo adduser <username> libvirt-qemu
```

# Configure the Network Bridge

Open /etc/network/interfaces in a text editor. Depending on your current network interface, update the document to look like the block below. **NOTE:** Replace interface "enp6s0" with the interface of the computer you are using to access the internet.

```
# interfaces(5) file used by ifup(8) and ifdown(8)
auto lo br0
iface lo inet loopback

iface enp6s0 inet manual

iface br0 inet dhcp
        bridge_ports enp6s0
```
Then, resestart the network by running the command below. **NOTE:** This will momentarilly disconnect your network interface.

```
sudo systemctl restart networking
```

# Setting up the VM

This is intuative. Read guide above for more info.