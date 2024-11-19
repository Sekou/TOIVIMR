#2024, S. Diane, tensorflow/keras neural network example

import tensorflow as tf
import numpy as np
from numpy.distutils.system_info import system_info


def categorize(symbol, symbols):
    v = np.zeros(len(symbols))
    i = symbols.index(symbol)
    v[i] = 1
    return v

def decode(out, symbols):
    return symbols[np.argmax(out)]

def createModel(ndims):
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(units=ndims, input_shape=[1, ndims]),
        # tf.keras.layers.Dense(units=ndims, activation='tanh', input_shape=[ndims]),
        tf.keras.layers.Dense(units=ndims, activation=tf.nn.softmax)
    ])
    return model


def trainNet(model, X_train, Y_train, X_val, Y_val):
    model.summary()

    model.compile(optimizer='adam', loss='categorical_crossentropy')

    losses = model.fit(X_train, Y_train,
                       validation_data=(X_val, Y_val),
                       batch_size=5,
                       epochs=50)

    result=model.predict(np.array([X_train[0]]))
    print(result)
