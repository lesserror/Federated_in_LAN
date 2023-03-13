#!coding=utf-8

import numpy as np
from tensorflow import keras
from ModelTrain import Model_json_load, Model_train
from SocketCommunicate import socket_connect, socket_client_send, socket_client_receive
import os
import time
import socket

os.environ["CUDA_VISIBLE_DEVICES"]="0"
if __name__ == '__main__':
    IPConfig = '192.168.1.60'
    Port_init = 1234
    Port_s = 9001
    Port_r = 9002
    SaveFilePath = './Data/'
    JsonFilePath = './Data/model_architecture.json'
    ReceiveWeightPath = './Data/Weight/'
    GlobalWeightPath = './Data/Weight/model_weight.npy'
    LocalWeightPath = './Data/Weight/Local/'
    ClientItem = 0

    # Init
    s_init = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_connect(IPConfig, Port_init, s_init)
    socket_client_receive(s_init, SaveFilePath)
    s_init.close()
    Model = Model_json_load(JsonFilePath)
    Model.compile(optimizer=keras.optimizers.Adam(1e-4), loss='categorical_crossentropy', metrics=['accuracy'])
    print("初始化结束")
    # train
    for count in range(10):
        s_r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_connect(IPConfig, Port_r, s_r)
        socket_client_receive(s_r, ReceiveWeightPath)
        s_r.close()
        print("接收weight结束")
        #time.sleep(2)
        
        Weight = np.array(np.load(GlobalWeightPath, allow_pickle=True), dtype=object)
        Model.set_weights(Weight)
        Model_train(Model, count, LocalWeightPath, ClientItem)
        
        s_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_connect(IPConfig, Port_s, s_s)
        socket_client_send(s_s, LocalWeightPath + "Client_" + str(ClientItem) + "_" + str(count)+".npy")
        print("发送weight结束")
        s_s.close()
        #time.sleep(3)

    # Close the socket
