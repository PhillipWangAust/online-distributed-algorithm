#!/usr/bin/env python
# -*- coding: utf-8 -*-

'a server example which send hello to client.'

import time, socket, threading
import json
from detect import *
from initialize import *
def tcplink(sock, addr):
    print 'Accept new inform connection from %s:%s...' % addr
    sock.send('Welcome!')
    Reboot_flag =False
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            break
        #########################
        else:
            data= json.loads(data)
            Reboot_flag =data['flag']
            with open('neighbour.json','r') as f:
                json_neighbour_list=json.load(f)
        
            neighbour_list=json_neighbour_list['neighbour']
        
            MAC_flag =True
            for node in neighbour_list:
                if data['MAC'] == node[1]:
                    #print data['MAC']
                    #print node[1]
                    node[0]=addr[0]
                    MAC_flag =False
            if MAC_flag:
                neighbour_list.append([addr[0],data['MAC']])
        
            json_neighbour_list={'neighbour':neighbour_list}
            with open('neighbour.json','w') as f:
                json.dump(json_neighbour_list,f)
 ##################
            sendmsg={'MAC':get_mac_address()}
            #print sendmsg
            sock.send(json.dumps(sendmsg))
    sock.close()
    print 'Connection from %s:%s closed.' % addr
    if Reboot_flag:
        os.system("for i in `ps -ef|grep python|awk '{print $2}' `; do kill -9 $i ; done;chmod+x initialze.py;./initialize.py")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 监听端口:
s.bind((get_ip_address(), 10001))
s.listen(5)
print 'Waiting for inform_client connection...'
while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()

