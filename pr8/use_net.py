import numpy as np
import cv2

import network

net = network.make_net()
net.load_weights("net.h5")

scene = cv2.imread("images\\scene.png")

arr = np.asarray(scene)

sz = network.sz
step = sz//5

def getCenter(img):
    mx, my, sx, sy=0,0,0,0
    for iy in range(0, img.shape[0]):
        for ix in range(0, img.shape[1]):
            v=255 - sum(img[iy,ix])/3
            mx+=v*ix
            my+=v*iy
            sx+=v
            sy+=v
    mx/=sx
    my/=sy
    return [mx, my]


for iy in range(0, arr.shape[0]-sz, step):
    print(f"y={iy} of {arr.shape[0]-sz}")
    for ix in range(0, arr.shape[1]-sz, step):
        input=arr[iy:iy+sz, ix:ix+sz]
        input=np.reshape(input, (1, sz, sz, network.nchannels))
        predictions = net.predict(input)[0]
        ind=np.argmax(predictions)
        cx, cy=getCenter(input[0])
        #для центровки образа
        d=max(abs(cx-input.shape[1]//2), abs(cy-input.shape[1]//2))

        if ind<2 and predictions[ind]>0.99 and predictions[2]<0.5 and d<3:
            color=(255,0,0) if ind==0 else (0,255,0)
            cv2.rectangle(scene, (ix, iy), (ix+sz, iy+sz), color, 1)

cv2.imwrite("result.png", scene)