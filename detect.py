#!/usr/bin/env python 
# _*_ coding=utf-8 _*_ 
from scapy.all import * 
import sys,getopt
import socket
import uuid
import fcntl
import struct

def get_ip_address(ifname = 'wlan0' ):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def get_mac_address():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

def detect_neighbour(iprange,ipfreq=2):
    #iprange means the range of ip ,ipfreq means the scan times of every ip
    neighbour_list=[]
    
    for ipFix in range(1,iprange):
        ip = "192.168.1.10"+str(ipFix)
        
        for i in range(1,ipfreq):
            arpPkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip, hwdst="ff:ff:ff:ff:ff:ff")
            res = srp1(arpPkt, timeout=1, verbose=0)
            
            if res:
                print "IP: " + res.psrc + "     MAC: " + res.hwsrc
                node=[res.psrc,res.hwsrc]
                if node not in neighbour_list:
                    neighbour_list.append(node)
                    #print neighbour_list
    return neighbour_list