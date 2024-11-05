import numpy as np
import cv2

import network

net = network.make_net()
net.load_weights("net.h5")

scene = cv2.imread("images\\scene.png")

arr = np.asarray(scene)

sz = network.sz
step = sz//5

for iy in range(0, arr.shape[0]-sz, step):
    print(f"y={iy} of {arr.shape[0]-sz}")
    for ix in range(0, arr.shape[1]-sz, step):
        input=arr[iy:iy+sz, ix:ix+sz]
        input=np.reshape(input, (1, sz, sz, network.nchannels))
        predictions = net.predict(input)[0]
        ind=np.argmax(predictions)
        if ind<2 and predictions[ind]>0.99 and predictions[2]<0.5:
            color=(255,0,0) if ind==0 else (0,255,0)
            cv2.rectangle(scene, (ix, iy), (ix+sz, iy+sz), color, 1)

cv2.imwrite("result.png", scene)