#FAST example
import cv2
import numpy as np

img=cv2.imread("img.jpg")
cv2.imshow("img", img)


print(f"Image Size: {img.shape}")

deltas=[[0,-3], [1,-3], [2,-2], [3,-1], [3, 0], [3,1], [2,2],
        [1,3], [0,3], [-1,3], [-2,2], [-3,1], [-3,0], [-3,-1], [-2,-2], [-1,-3]]

def getPx(img, x, y):
    if x<0 or y<0 or x>=img.shape[1] or y>=img.shape[0]:
        return [0,0,0]
    return img[y, x]

def getDescr(img, x, y):
    thr = 20
    descr=[]
    px=getPx(img, x, y)
    v=np.sum(px)/3
    n1, n2, n3 = 0, 0, 0
    for d in deltas:
        px2=getPx(img, x+d[0], y+d[1])
        v2 = np.sum(px2) / 3
        if v2>v+thr: #крайний пиксель светлее центра
            n1+=1; n2, n3 = 0, 0
            descr.append(0)
        if v2<v-thr: #крайний пиксель темнее центра
            n2+=1; n1, n3 = 0, 0
            descr.append(1)
        if v+thr>v2>v-thr: #крайний пиксель похожий
            n3+=1; n1, n2 = 0, 0
            descr.append(2)
    if max([n1, n2])>=12:
        return descr
    else:
        return None

def getFeatureMap(img):
    fm=np.zeros(img.shape)
    for iy in range(img.shape[0]):
        print(iy)
        for ix in range(img.shape[1]):
            fm[iy, ix]=[255, 255, 255] \
            if getDescr(img, ix, iy) is not None \
            else [0,0,0]
    return fm

fm=getFeatureMap(img)
cv2.imwrite("fm.jpg", fm)
cv2.imshow("fm", fm)


cv2.waitKey(0)