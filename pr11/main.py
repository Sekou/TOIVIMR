import numpy as np

map=np.zeros((5,6))
map[1,1]=1
map[1,2]=1
map[1,3]=1
map[2,3]=1
map[3,3]=1


rewards=np.zeros((5,6))
rewards[0,5] = 1
rewards-=map

vals=np.array(rewards)
print(map)
print(rewards)

pos=[4,0]

def iterValues(vals, rewards, gamma=0.7, alpha=0.3):
    vals2=np.array(vals)
    for ix in range(vals.shape[1]):
        for iy in range(vals.shape[0]):
            if rewards[iy,ix]!=0:
                continue
            #цикл по окрестности ячеек
            vv=[]
            for j,k in [[-1, 0], [-1,-1], [0, -1], [1, -1], [1, 0], [1,1], [0, 1], [-1,1]]:
                ix_,iy_=ix+j, iy+k
                if ix_<0 or ix_>=vals.shape[1]: continue
                if iy_<0 or iy_>=vals.shape[0]: continue
                vv.append(vals[iy_,ix_])
            d=alpha*(rewards[iy,ix] + gamma*max(vv) - vals[iy,ix])
            vals2[iy,ix]=d
    return vals2

def getNestPos(vals, ix0, iy0):
    bestPos=None
    maxVal=vals[iy0, ix0]
    for j, k in [[-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1]]:
        ix_, iy_ = ix0 + j, iy0 + k
        if ix_ < 0 or ix_ >= vals.shape[1]: continue
        if iy_ < 0 or iy_ >= vals.shape[0]: continue
        if vals[iy_,ix_]>maxVal:
            bestPos=[ix_, iy_]
            maxVal=vals[iy_,ix_]
    return bestPos

def getTraj(ix0, iy0):
    res=[]
    p=[ix0, iy0]
    while True:
        res.append(p)
        p=getNestPos(vals, *p)
        if p is None:
            break
    return res

for i in range(30):
    vals=iterValues(vals, rewards, 0.7, 0.3)
    print("Changing vals:")
    print(vals)
print(vals)

print("Traj from 0,0:")
print(getTraj(0,0))
print("Traj from 0,4:")
print(getTraj(0,4))


