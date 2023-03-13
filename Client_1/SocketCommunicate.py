#!coding=utf-8

import socket
import os
import sys
import struct
import time


def socket_connect(ipconfig, port, S):
    """
    An TCP connection to the server

    通信建立（TCP，面向连接）

    :param ipconfig: server ip; 服务器IP
    :param port: server port; 服务器端口
    :return: socket s; 与服务器的socket
    """
    try:
    # while True:
        # AF_INET:TCP通信
        # SOCK_STREAM： 面向连接的
        #S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        S.connect((ipconfig, port))

    except socket.error as msg:
        print("Waiting for connection...")
        time.sleep(2)
        socket_connect(ipconfig, port, S)
    #     sys.exit(1)
    return S


def socket_client_send(S, Filepath):
    """
    Send the file at the Filepath to server through socket S

    通过与服务器的socket传输Filepath的单个文件

    :param S: socket to the server; 与服务器通信的socket
    :param Filepath: Path of the file send to server; 发送文件路径
    :return: None; 无返回值
    """
    # 判断是否为文件
    if os.path.isfile(Filepath):
        # 定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
        # 定义文件头信息，包含文件名和文件大小
        fhead = struct.pack('128sl', os.path.basename(Filepath).encode('utf-8'), os.stat(Filepath).st_size)
        # 发送文件名称与文件大小
        S.send(fhead)

        # 将传输文件以二进制的形式分多次上传至服务器
        fp = open(Filepath, 'rb')
        while 1:
            data = fp.read(1024)
            if not data:
                # print('{0} file send over...'.format(os.path.basename(Filepath)))
                break
            S.send(data)


def socket_client_receive(S, Filepath):
    """
    Receive one document from the server through socket S, the file is saved to the Filepath

    从服务器接收单个文件，存储到Filepath文件夹下

    :param S: Socket to the server; 与服务器通信的socket
    :param Filepath: Folder where received file saved; 接收存储文件的文件夹的路径
    :return: None; 无返回值
    """
    try:
        while 1:
            # 申请相同大小的空间存放发送过来的文件名与文件大小信息
            fileinfo_size = struct.calcsize('128sl')
            # 接收文件名与文件大小信息
            buf = S.recv(fileinfo_size)
            # 判断是否接收到文件头信息
            if buf:
                # 获取文件名和文件大小
                filename, filesize = struct.unpack('128sl', buf)
                fn = filename.strip(b'\00')
                fn = fn.decode()
                # print('file new name is {0}, filesize if {1}'.format(str(fn), filesize))
                recvd_size = 0  # 定义已接收文件的大小
                # 存储在该脚本所在目录下面
                fp = open(Filepath + str(fn), 'wb')
                # 将分批次传输的二进制流依次写入到文件
                while not recvd_size == filesize:
                    if filesize - recvd_size > 1024:
                        data = S.recv(1024)
                        recvd_size += len(data)
                    else:
                        data = S.recv(filesize - recvd_size)
                        recvd_size = filesize
                    fp.write(data)
                fp.close()
                # print('end receive')
                break
    except:
        print("Disconnect, receive fail!")
        S.close()
