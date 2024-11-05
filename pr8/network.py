nchannels=3 #RGB
nclasses=3 #крестики, нолики и пустота
sz=28 #размер 28*28 пикселей

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Flatten

def make_net():
    model = Sequential([
        Conv2D(filters=64, kernel_size=(5,5), activation="relu"),
        MaxPooling2D(pool_size=2),
        Flatten(),
        Dense(64, activation="relu"),
        Dense(nclasses, activation="softmax")
    ])
    model.build(input_shape=(1, sz, sz, nchannels))
    return model