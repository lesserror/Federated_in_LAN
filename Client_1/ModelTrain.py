#!coding=utf-8


import numpy as np
import json
import tensorflow as tf


def Model_json_load(path):
    """
    Load the model architecture without weight from json according to the Path (need to be optimized)

    从json文件加载tensorflow模型结构，不含权重（需要optimize）

    :param path: Path of the json file; json文件的路径
    :return: Tensorflow model; Tensorflow模型结构
    """
    with open(path, 'r') as f:
        model_json = json.load(f)
    model = tf.keras.models.model_from_json(model_json)
    return model


def Model_train(model, i, path, Item):
    """
    Firstly load the train data and label from the Dataset folder, then train the model and save the weight to Data folder

    首先根据i加载训练数据与标签，然后训练并存储训练参数文件到path路径

    :param model: tensorflow model (after optimized); Tensorflow模型（optimize之后）
    :param i: the i folder in Dataset (also the i federated epoch); 第i轮Federated Learning——Dataset的第i个文件夹
    :param path: The path of the weight document; 训练参数保存路径
    :return: None; 无返回值
    """
    train_data = np.load('Dataset/' + str(i) + '/' + 'train_data.npy')
    train_label = np.load('Dataset/' + str(i) + '/' + 'train_label.npy')
    model.fit(train_data, train_label, batch_size=32, epochs=5)
    weight = np.array(model.get_weights(), dtype=object)
    np.save(path+"Client_"+str(Item)+"_"+str(i)+".npy", weight)
