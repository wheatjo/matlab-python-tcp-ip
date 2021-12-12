import socket
import numpy as np
import json
# from progress.bar import Bar
import math
import scipy.io

#json解析numpy数据类
addr = ('127.0.0.1',30000) #设置服务端ip地址和端口号
buff_size = 65535         #消息的最大长度

tcpSerSock = socket.socket()
port = 30000
tcpSerSock.bind(addr)
tcpSerSock.listen(5)

while True:
    print('wait connecting ...')
    tcpCliSock, addr = tcpSerSock.accept() # 没有接收会一直等待
    print('connect to :', addr, 'try to read pop')
    while True:
        recv_data = []
        while not recv_data:
            recv_data = tcpCliSock.recv(100)
            # print(recv_data)
        
        assert recv_data == b'w', print("recv data is ", recv_data)
        pops = scipy.io.loadmat('pop.mat')
        pop_np = np.array(pops['pop'])
        print(pop_np)
        tcpCliSock.send('hru'.encode('utf-8')) # have read and use
        print("have send")
        break
    # tcpCliSock.close()
    
tcpSerSock.close()
