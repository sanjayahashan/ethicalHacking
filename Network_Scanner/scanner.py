#!usr/bin/env python

import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser(description="Displays the MAC addresses of a given IP using ARP")
    parser.add_argument('--target', dest='target', help="Target IP or IP range")
    options = parser.parse_args()
    return options

'''
    scans the given IP or IP range and returns a list containing dictionaries 
    of each IP and MAC address
'''
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)                           #create a ARP request
    # arp_request.show()        #can be used display info
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")           #create ether frame and set the broadcast MAC
    arp_request_broadcast = broadcast/arp_request              #combine ARP request and ether frame
    # arp_request_broadcast.show()
    # scapy.ls(scapy.ARP())     #list out class properties

    ans, unans = scapy.srp(arp_request_broadcast, timeout=1)   #used to send and recieve packets

    clients_list = []
    for element in ans:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)

    return clients_list

def print_result(results_list):
    print("IP\t\t\tMAC Address\n-----------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])

options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)
# scapy.arping("192.168.42.1/24")