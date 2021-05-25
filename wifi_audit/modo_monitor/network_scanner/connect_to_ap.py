import os
import subprocess
import time


def connect(ssid, password):

    try:
        proceso = subprocess.check_output(["nmcli device wifi connect %s password %s" % (ssid, password)], shell=True)
        time.sleep(1)
        if proceso != 1:
            new_ssid = subprocess.check_output("nmcli -f SSID,IN-USE dev wifi list | grep '*' | awk '{print $1}'",
                                               shell=True).decode('utf-8')
            new_bssid = subprocess.check_output("nmcli -f BSSID,IN-USE dev wifi list | grep '*' | awk '{print $1}'",
                                                shell=True).decode('utf-8')
            list = [new_ssid, new_bssid]
        else:
            list = []
    except:
        list = []

    return list


def check_connected(ssid):

    actual_ssid = subprocess.check_output("nmcli -f SSID,IN-USE dev wifi list | grep '*' | awk '{print $1}'",shell=True).decode('utf-8')[:-1]

    if actual_ssid == ssid:
        return 0
    else:
        return 1

def check_interfaces():

    interfaces = os.listdir("/sys/class/net")

    return interfaces


def check_interface_mode(modo):

    interfaces_list = []
    interfaces = os.listdir("/sys/class/net")
    if modo == "monitor":
        for interface in interfaces:
            mode = subprocess.check_output("cat /sys/class/net/%s/type" % interface, shell=True).decode('utf-8').rstrip(
                "\n")
            if mode == "803":
                interfaces_list.append(interface)

    elif modo == "managed":
        for interface in interfaces:
            mode = subprocess.check_output("cat /sys/class/net/%s/type" % interface, shell=True).decode('utf-8').rstrip(
                "\n")
            if mode == "1":
                interfaces_list.append(interface)

    return interfaces_list