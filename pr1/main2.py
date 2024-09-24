
import sys, pygame
import numpy as np
import math

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
def drawText(screen, s, x, y):
    surf=font.render(s, True, (0,0,0))
    screen.blit(surf, (x,y))

sz = (800, 600)

def rot(v, ang): #функция для поворота на угол
    s, c = math.sin(ang), math.cos(ang)
    return [v[0] * c - v[1] * s, v[0] * s + v[1] * c]

def limAng(ang):
    while ang > math.pi: ang -= 2 * math.pi
    while ang <= -math.pi: ang += 2 * math.pi
    return ang

def rotArr(vv, ang): # функция для поворота массива на угол
    return [rot(v, ang) for v in vv]

def dist(p1, p2):
    return np.linalg.norm(np.subtract(p1, p2))

def drawRotRect(screen, color, pc, w, h, ang): #точка центра, ширина высота прямоуг и угол поворота прямогуольника
    pts = [
        [- w/2, - h/2],
        [+ w/2, - h/2],
        [+ w/2, + h/2],
        [- w/2, + h/2],
    ]
    pts = rotArr(pts, ang)
    pts = np.add(pts, pc)
    pygame.draw.polygon(screen, color, pts, 2)

pts = [
    [100, 100],
    [200, 160],
    [300, 190],
    [400, 270],
    [500, 310],
    [600, 340],
    [700, 420],

    [150, 100],
    [370, 320],
    [600, 450]
]

checks=[True]*len(pts)


k=1
b=0
P1=None
P2=None

thr = 50 # порог

variants=set()

def drawLine(screen):
    p1 = [0, k*0+b]
    p2 = [800, k*800+b]
    pygame.draw.line(screen, (0,255,0), p1, p2, 3)

    alpha=math.atan(k)
    dy=thr/math.cos(alpha)

    pygame.draw.line(screen, (0,255,0), [p1[0], p1[1]-dy], [p2[0], p2[1]-dy], 1)
    pygame.draw.line(screen, (0,255,0), [p1[0], p1[1]+dy], [p2[0], p2[1]+dy], 1)

def calcMSE():
    res=0
    for p in pts:
        dy = p[1] - (k*p[0]+b)
        res+=dy*dy
    return res/len(pts)

def RANSAC():
    global k, b, P1, P2

    #подвыборка инлаеров
    pts_=[p for i,p in enumerate(pts) if checks[i]]

    if len(pts_)<2: return

    #выбор случайных точек данных среди инлаеров
    i1=np.random.randint(0,len(pts_)-1)
    i2=np.random.randint(i1+1,len(pts_))
    p1=P1=pts_[i1]
    p2=P2=pts_[i2]

    #оценка параметров модели (прямой линии)
    dx=p2[0]-p1[0]
    dy=p2[1]-p1[1]
    if dx==0: dx=0.0000001
    k_=dy/dx
    b_=p1[1]-k_*p1[0]

    #обновление коффициентов
    k, b = k_, b_
    e=calcMSE()
    print(k, b, e)
    variants.add((k, b, e))

    #пересчет релевантности точек
    checkPts(thr)

def selectBest():
    #определяем индекс лучшего варианта
    l=list(variants)
    i=np.argmin([v[2] for v in l])
    return l[i][:2]

def calcPtDist(p, k, b):
    return np.abs(-k*p[0]+p[1]-b)/math.sqrt(k*k+1)

def checkPts(thr):
    for i, p in enumerate(pts):
        d=calcPtDist(p, k, b)
        checks[i] = d<thr

def main():
    global k, b

    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1:
                    checkPts(thr)
                    print("Distances:")
                    for p in pts:
                        d=calcPtDist(p, k, b)
                        print(d)
                if ev.key == pygame.K_2:
                    RANSAC()
                if ev.key == pygame.K_3:
                    k, b=selectBest()
                    checkPts(thr)
                if ev.key == pygame.K_4:
                    d=calcPtDist([6, 4], 1, 0)
                    print("d=", d)

        dt=1/fps

        screen.fill((255, 255, 255))

        for i, p in enumerate(pts):
            #синий цвет, если точка - инлаер
            color = (0,0,255) if checks[i] else (255,0,0)
            pygame.draw.circle(screen, color, p, 5, 2)

        if P1 is not None and P2 is not None:
            pygame.draw.circle(screen, (255, 0, 0), P1, 10, 1)
            pygame.draw.circle(screen, (255, 0, 0), P2, 10, 1)

        mse=calcMSE()
        drawText(screen, f"MSE = {mse}", 5, 5)
        drawLine(screen)

        pygame.display.flip()
        timer.tick(fps)

main()

#template file by S. Diane, RTU MIREA, 2024