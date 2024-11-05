import glob
import numpy as np
from random import shuffle
import cv2
import network

train_images=[]
train_labels=[]

#крестики
for filename in glob.glob("images\\X\\*.png"):
    img = cv2.imread(filename)
    train_images.append(np.asarray(img))
    train_labels.append([1, 0, 0])
#нолики
for filename in glob.glob("images\\O\\*.png"):
    img = cv2.imread(filename)
    train_images.append(np.asarray(img))
    train_labels.append([0, 1, 0])
#шумы
for i in range(len(train_images)):
    v0=np.random.randint(210,254)
    v1=np.random.randint(v0+1,255)
    img = np.random.randint(v0, v1, 3*network.sz**2, dtype=int)
    img = np.reshape(img, (network.sz, network.sz, network.nchannels))
    train_images.append(img)
    train_labels.append([0, 0, 1])

#перемешивание примеров
inds=np.arange(len(train_images), dtype=int)
shuffle(inds)
train_images=[train_images[i] for i in inds]
train_labels=[train_labels[i] for i in inds]

nsamples=len(train_images)
train_images=np.reshape(train_images,
                        (nsamples, network.sz, network.sz, network.nchannels))
train_labels=np.reshape(train_labels,
                        (nsamples, network.nclasses))

net = network.make_net()

net.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

net.fit(train_images, train_labels, batch_size=5, epochs=3)

net.save_weights("net.h5")

