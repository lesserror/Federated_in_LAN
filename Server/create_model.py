import json
import tensorflow as tf
from tensorflow.keras import layers


def create_Alex(inputs):
    x = layers.Conv1D(filters=48, kernel_size=(11,), strides=4, padding='same', activation='relu')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling1D(pool_size=2, strides=2, padding='valid')(x)
    x = layers.Conv1D(filters=128, kernel_size=(5,), padding='same', activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling1D(pool_size=3, strides=2, padding='valid')(x)
    x = layers.Conv1D(filters=192, kernel_size=(3,), padding='same', activation='relu')(x)
    x = layers.Conv1D(filters=192, kernel_size=(3,), padding='same', activation='relu')(x)
    x = layers.Conv1D(filters=128, kernel_size=(3,), padding='same', activation='relu')(x)
    x = layers.MaxPooling1D(pool_size=3, strides=2, padding='valid')(x)
    x = layers.GlobalAveragePooling1D(name='pooling611')(x)
    return x


def Model_structure(Shape, ClassNum):
    inputs = layers.Input(Shape)
    x = create_Alex(inputs)
    x = layers.Dense(units=256, activation='relu', name='dense1')(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(units=ClassNum, activation='softmax', name='dense2')(x)
    return tf.keras.models.Model(inputs, x)


if __name__ == '__main__':
    CreateModel = Model_structure([5120, 1], 16)
    model_json = CreateModel.to_json()
    name = 'CreateModel.json'
    with open(name, 'w') as f:
        json.dump(model_json, f)
