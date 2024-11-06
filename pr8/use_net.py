import numpy as np
import cv2
import network

net = network.make_net()
net.load_weights("net.h5")

scene = cv2.imread("images\\scene.png")
arr = np.asarray(scene)

def getCenter(img):
    mx, my, mass=0,0,0
    for iy in range(0, img.shape[0]):
        for ix in range(0, img.shape[1]):
            v=255 - sum(img[iy,ix])/3
            mx+=v*ix
            my+=v*iy
            mass+=v
    return [mx/mass, my/mass]

sz = network.sz
step = sz//5
fragments=[]
for iy in range(0, arr.shape[0]-sz, step):
    for ix in range(0, arr.shape[1]-sz, step):
        input=arr[iy:iy+sz, ix:ix+sz]
        fragments.append(input)

inputs=np.reshape(fragments, (len(fragments), sz, sz, network.nchannels))
predictions = net.predict(inputs)

i=0
for iy in range(0, arr.shape[0]-sz, step):
    for ix in range(0, arr.shape[1]-sz, step):
        pred=predictions[i]
        ind=np.argmax(pred)
        c = getCenter(fragments[i])
        d = np.linalg.norm(np.subtract(c, [sz / 2, sz / 2]))
        if ind<2 and pred[ind]>0.99 and pred[2]<0.5 and d<4:
            color=(255,0,0) if ind==0 else (0,255,0)
            cv2.rectangle(scene, (ix, iy), (ix+sz, iy+sz), color, 1)
        i+=1

cv2.imwrite("result.png", scene)