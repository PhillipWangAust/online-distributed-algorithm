#!/usr/bin/env python
# -*- coding: utf-8 -*-

'a server example which send hello to client.'

import time, socket, threading
import json
from detect import *

def tcplink(sock, addr):
    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            break
        if data == 'get_neighbour':
            with open('neighbour.json','r') as f:
                sendmsg=json.load(f)
            sendmsg['MAC']=get_mac_address()
            print sendmsg
            sock.send(json.dumps(sendmsg))
    sock.close()
    print 'Connection from %s:%s closed.' % addr

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 监听端口:
s.bind((get_ip_address(), 10002))
s.listen(5)
print 'Waiting for get neighbour client connection...'
while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
    #s.shutdown(2)
    time.sleep(15)
    #s.listen(5)
