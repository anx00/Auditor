import json
import os, subprocess

# Transform decimal data to Binary
def decimalToBinary(n):
    return "{0:b}".format(int(n))


# Filter noise MAC Addresses such as broadcast, multicast, STP.
def noise_filter(addr1, addr2):
    # Broadcast, multicast, STP...
    ignore = ['ff:ff:ff:ff:ff:ff', '00:00:00:00:00:00', '33:33:00:', '33:33:ff:', '01:80:c2:', '01:00:5e:', '01:1b:19:',
              '01:0c:cd:', '01:00:0c:']

    if addr1 is not None and addr2 is not None:
        for i in ignore:
            if i in addr1 or i in addr2:
                return True


# Function to get the Manufacturer given the MAC
def manf2(mac):
    with open('mac-vendors-export.json') as f:
        vendor = json.load(f)

    for p in vendor:
        if p['macPrefix'] == mac:
            return p['vendorName']

    return "Unknown"


#Check if interface is in Monitor Mode
def check_interface():
    interfaces = os.listdir("/sys/class/net")
    for interface in interfaces:
        mode = subprocess.check_output("cat /sys/class/net/%s/type" % interface, shell=True).decode('utf-8').rstrip(
            "\n")
        if mode == "803":
            return interface


#Function to restart interface
def restart_interface():
    os.system("restartCard >/dev/null 2>&1")


#Convert a list to a string
def convert_list_to_string(org_list, seperator=' '):
    """ Convert list to string, by joining all item in list with given separator.
        Returns the concatenated string """
    return seperator.join(org_list)
