#!coding=utf-8
import os
import socket
import struct
import threading

import numpy as np
import time
import random

def socket_server_receive(C, Filepath):
    try:
        while True:
            # 申请相同大小的空间存放发送过来的文件名与文件大小信息
            fileinfo_size = struct.calcsize('128sl')
            # 接收文件名与文件大小信息
            buf = C.recv(fileinfo_size)
            # 判断是否接收到文件头信息
            if buf:
                # 获取文件名和文件大小
                filename, filesize = struct.unpack('128sl', buf)
                fn = filename.strip(b'\00')
                fn = fn.decode()
                print('file new name is {0}, filesize if {1}'.format(str(fn), filesize))
                recvd_size = 0  # 定义已接收文件的大小
                # 存储在该脚本所在目录下面
                fp = open(Filepath + str(fn), 'wb')
                print('start receiving from client')
                # 将分批次传输的二进制流依次写入到文件
                while not recvd_size == filesize:
                    if filesize - recvd_size > 1024:
                        data = C.recv(1024)
                        recvd_size += len(data)
                    else:
                        data = C.recv(filesize - recvd_size)
                        recvd_size = filesize
                    fp.write(data)
                fp.close()
                print('end receive')
                break
    except:
        print("Disconnect")
        C.close()


def socket_server_send(C, Filepath):
    """
    Send the file at the Filepath to client through socket C

    通过与Client的socket传输Filepath的单个文件

    :param C: socket to the client; 与Client通信的socket
    :param Filepath: Path of the file send to server; 发送文件路径
    :return: None; 无返回值
    """
    # 判断是否为文件
    time.sleep(random.uniform(0.000,0.020))
    if os.path.isfile(Filepath):
        # 定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
        # 定义文件头信息，包含文件名和文件大小
        fhead = struct.pack('128sl', os.path.basename(Filepath).encode('utf-8'), os.stat(Filepath).st_size)
        # 发送文件名称与文件大小
        C.send(fhead)
        # 将传输文件以二进制的形式分多次上传至服务器
        fp = open(Filepath, 'rb')
        while 1:
            data = fp.read(1024)
            if not data:
                print('{0} file send over...'.format(os.path.basename(Filepath)))
                break
            C.send(data)


def FedAvg(Path):
    num = 0
    for Item in os.listdir(Path):
        if num == 0:
            weight = np.load(Path + Item, allow_pickle=True)
        else:
            weight = weight + np.load(Path + Item, allow_pickle=True)
        num = num + 1
    weight = weight / num
    np.save('./Data/model_weight.npy', weight)


def socket_service():
    ClientNum = 2
    SaveFilePath = './Data/WeightFromClient/'
    JsonFilePath = './Data/OriginFile/model_architecture.json'
    WeightFilePath = './Data/model_weight.npy'
    OriginWeightPath = './Data/OriginFile/model_weight.npy'
    LoopCount = 0
    # Init
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Init_S:
        Init_S.bind(("192.168.1.60", 1234))
        Init_S.listen()  # 将socket置为监听状态，等待客户端的连接
        while True:
            Init_thread_list = []
            for i in range(ClientNum):
                i_c, i_addr = Init_S.accept()  # accept会接受来自任意客户端的连接，并返回一个新的socket---c和客户端的IP地址addr
                Init_thread = threading.Thread(target=socket_server_send, args=(i_c, JsonFilePath))
                Init_thread.start()
                Init_thread_list.append(Init_thread)
            for Init_thread in Init_thread_list:
                Init_thread.join()  # 等待当前线程的任务执行完毕再向下继续执行
            break
    # Loop, 先发再收
    print("Init Clear")
    while True:
        WeightPath_Epoch = SaveFilePath + "/" + str(LoopCount) + "/"
        # 创建另一个socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_S:
            send_S.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            send_S.bind(("192.168.1.60", 9002))
            send_S.listen()  # 将socket置为监听状态，等待客户端的连接
            while True:
                send_thread_list = []
                for j in range(ClientNum):
                    s_c, s_addr = send_S.accept()  # accept会接受来自任意客户端的连接，并返回一个新的socket---c和客户端的IP地址addr
                    if LoopCount == 0:
                        send_thread = threading.Thread(target=socket_server_send, args=(s_c, OriginWeightPath))
                    else:
                        send_thread = threading.Thread(target=socket_server_send, args=(s_c, WeightFilePath))
                    send_thread.start()
                    send_thread_list.append(send_thread)
                for send_thread in send_thread_list:
                    send_thread.join()  # 等待当前线程的任务执行完毕再向下继续执行
                print("Send Clear, Round: " + str(LoopCount + 1))
                break

        # 创建一个socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receive_S:
            receive_S.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            receive_S.bind(("192.168.1.60", 9001))
            receive_S.listen()  # 将socket置为监听状态，等待客户端的连接
            while True:
                receive_thread_list = []
                for i in range(ClientNum):
                    r_c, r_addr = receive_S.accept()  # accept会接受来自任意客户端的连接，并返回一个新的socket---c和客户端的IP地址addr
                    receive_thread = threading.Thread(target=socket_server_receive, args=(r_c, WeightPath_Epoch))
                    receive_thread.start()
                    receive_thread_list.append(receive_thread)
                for receive_thread in receive_thread_list:
                    receive_thread.join()  # 等待当前线程的任务执行完毕再向下继续执行
                print("Receive Clear, Round: " + str(LoopCount + 1))
                break
        FedAvg(WeightPath_Epoch)
        LoopCount = LoopCount + 1
        print("Calculate Clear, Round: " + str(LoopCount))
        time.sleep(60)


# 全局变量要加锁
if __name__ == "__main__":

    socket_service()
