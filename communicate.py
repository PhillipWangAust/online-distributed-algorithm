#!/usr/bin/env python 
# _*_ coding=utf-8 _*_ 
import socket
import json
from detect import *

def second_neighbour_detect_client(neighbour_list):
    ip_local=get_ip_address()
    mac_local=get_mac_address()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    second_neighbour_list=[]
    
    while neighbour_list:
        s.connect((neighbour_list[0][0], 10002))
        print s.recv(1024)
        s.send('get_neighbour')
        
        recvmsg=s.recv(1024)
        print recvmsg
        recvmsg=json.loads(recvmsg)
        if [neighbour_list[0][0],recvmsg['MAC']] in neighbour_list :
            neighbour_list.remove([neighbour_list[0][0],recvmsg['MAC']])
            second_neighbour_list+=recvmsg['neighbour']
            
            if [ip_local,mac_local] in second_neighbour_list:
                second_neighbour_list.remove([ip_local,mac_local])
        
        
        
        s.send('exit')
        s.close()
        
    return second_neighbour_list

def inform_neighbour_client(neighbour_list):
    mac_local=get_mac_address()
    ip_neighbour_list=[x[0] for x in neighbour_list ]
    print ip_neighbour_list
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while neighbour_list:
        s.connect((neighbour_list[0][0], 10001))
        
        ip_neighbour_list.remove(neighbour_list[0][0])
        
        if neighbour_list[0][0] in ip_neighbour_list :
            flag = True #need change
        else:
            flag =False
        
        print s.recv(1024)
        
        sendmsg={'flag':flag,'MAC':mac_local}
        print sendmsg
        
        s.send(json.dumps(sendmsg))
        
        recvmsg=s.recv(1024)
        
        print recvmsg
        
        recvmsg=json.loads(recvmsg)
        
        if [neighbour_list[0][0],recvmsg['MAC']] in neighbour_list :
            neighbour_list.remove([neighbour_list[0][0],recvmsg['MAC']])
            
        
        s.send('exit')
        s.close()



    
    