#!usr/bin/env python

import subprocess   #subprocess module used to execute system commands
import optparse     #optparse module pass command line arguments
import re           #regular expressios


'''
    this function is used to get the command line arguments
'''
def get_args():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")

    (options, interface) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface to change")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC")
    return options

'''
    this function is used to change the MAC
'''
def change_mac(interface, new_mac):
    print("[+] Changing MAC address of " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])                    #first it is required to disable the selected interface before changing the MAC address
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])    #change the MAC
    subprocess.call(["ifconfig", interface, "up"])                      #enable the interface

'''
    this function returns the MAC address of the given interface
    * used for display purposes
'''
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_search_result:
        return mac_search_result.group(0)
    else:
        print("[-] Couldn't read MAC Address.")

options = get_args()
# change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
print("current MAC : " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac==options.new_mac:
    print("[+] MAC address changed successfully to " + current_mac)
else:
    print("[-] Unable to change MAC address")
