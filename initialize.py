#!/usr/bin/env python 
# _*_ coding=utf-8 _*_ 
from detect import *
from communicate import *
import os
import json
import copy

def re_coloring():
    os.system("ifconfig wlan0 192.168.1.254")
    iprange=10
    ipfreq = 2
    neighbour_list=detect_neighbour(iprange,ipfreq)
    ip_neighbour_set={x[0] for x in neighbour_list}
    
    json_neighbour_list={'neighbour':neighbour_list}
    with open('neighbour.json','w') as f:
        json.dump(json_neighbour_list,f)
    #with open('config.json','r') as f:
    #    data=json.load(f)    
    #print data
    second_neighbour_list=second_neighbour_detect_client(neighbour_list)
    ip_second_neighbour_set={x[0] for x in second_neighbour_list}

    json_second_neighbour_list={'second_neighbour':second_neighbour_list}

    with open('second_neighbour.json','w') as f:
        json.dump(json_second_neighbour_list,f)
        
    existed_ip_set=ip_neighbour_set | ip_second_neighbour_set

    for ipFix in range(1,iprange):
            ip = "192.168.1.10"+str(ipFix)
            if ip not in existed_ip_set:
                break
    os.system("ifconfig wlan0 "+ip)

def initialization():
    os.system("ifconfig wlan0 192.168.1.254")
    iprange=10
    ipfreq = 2
    neighbour_list=detect_neighbour(iprange,ipfreq)
    ip_neighbour_set={x[0] for x in neighbour_list}
    
    json_neighbour_list={'neighbour':neighbour_list}
    with open('neighbour.json','w') as f:
        json.dump(json_neighbour_list,f)
    #with open('config.json','r') as f:
    #    data=json.load(f)    
    #print data
    second_neighbour_list=second_neighbour_detect_client(copy.deepcopy(neighbour_list))
    ip_second_neighbour_set={x[0] for x in second_neighbour_list}

    json_second_neighbour_list={'second_neighbour':second_neighbour_list}

    with open('second_neighbour.json','w') as f:
        json.dump(json_second_neighbour_list,f)
        
    existed_ip_set=ip_neighbour_set | ip_second_neighbour_set

    for ipFix in range(1,iprange):
            ip = "192.168.1.10"+str(ipFix)
            if ip not in existed_ip_set:
                break
    os.system("ifconfig wlan0 "+ip)
    
    #inform_neighbor
    print neighbour_list
    inform_neighbour_client(copy.deepcopy(neighbour_list))
    
    os.system("python get_neighbour_server.py & python inform_server.py")
if __name__ == '__main__':
    
    initialization()