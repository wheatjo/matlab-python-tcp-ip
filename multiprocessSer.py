from multiprocessing import Process, Queue, Lock
import socket
import numpy as np
import json
# from progress.bar import Bar
import math
import scipy.io
import logging



class Server(Process):

    def __init__(self, ser_que, lock, addr=('127.0.0.1',30000)):
        super().__init__()
        self.tcpSerSock = socket.socket()
        self.tcpSerSock.bind(addr)
        self.tcpSerSock.listen(2)
        self.io = scipy.io
        self.que = ser_que
        self.lock = lock
        print("Server ")

    def run(self):
        while True:
            print('wait connecting ...')
            tcpCliSock, addr = self.tcpSerSock.accept() # 没有接收会一直等待
            print('connect to :', addr, 'try to read pop')
            while True:
                recv_data = []
                while not recv_data:
                    recv_data = tcpCliSock.recv(100)
                    # print(recv_data)
                
                # get pop state = p | get reward = r
                logging.debug("receive data is %s", recv_data)
                assert (recv_data == b'p' or recv_data == b'r'), print("recv data is ", recv_data)
                # pops = self.io.loadmat('pop.mat')
                # pop_np = np.array(pops['pop'])
                # print(pop_np)
                self.lock.acquire()
                if recv_data == b'p':
                    self.que.put('pop state')
                    pops = self.io.loadmat('pop.mat')
                    pop_np = np.array(pops['pop'])
                    self.que.put(pop_np)

                else:
                    self.que.put('read reward')
                    reward = self.io.loadmat('reward.mat')
                    reward_np = np.array(reward['reward'])
                    self.que.put(reward_np)

                self.lock.release()
                tcpCliSock.send('hru'.encode('utf-8')) # have read and use
                print("have send")
                break
            
            tcpCliSock.close()


class SimTrain(Process):

    def __init__(self, que, lock):
        super().__init__()
        self.reward = None
        self.pop_state = None
        self.que = que
        self.lock = lock
        print("SimTrain")

    def run(self):
        print("run simtrainer")
        while True:
            while not self.que.empty():
                self.lock.acquire()
                flag = self.que.get()
                logging.debug("trainer get flag is %s", flag)
                if flag == 'pop state':
                    self.pop_state = self.que.get()
                    print('pop state', self.pop_state)
                elif flag == 'read reward':
                    self.reward = self.que.get()
                    print("reward: ", self.reward)
                else:
                    raise Exception("quene error !")
                self.lock.release()
        




if __name__ == '__main__':
    logging.basicConfig(filename='myapp.log', level=logging.DEBUG)
    logging.getLogger(__name__)
    q = Queue()
    lock = Lock()
    # server = Process(target=Server, args=(q, lock), name="server")
    # trainer = Process(target=SimTrain, args=(q, lock), name="trainer")
    server = Server(q, lock)
    trainer = SimTrain(q, lock)
    trainer.start()
    server.start()
    # print(q.get())    # prints "[42, None, 'hello']"
    trainer.join()
    server.join()
