#TODO: реализовать загрузку и кластеризацию файлов pts1.txt и pts2.txt
#TODO: обеспечить автоматическое определение наилучшего числа кластеров

import sys, pygame
import numpy as np
import math

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
def drawText(screen, s, x, y):
    surf=font.render(s, True, (0,0,0))
    screen.blit(surf, (x,y))

def dist(p1, p2):
    return np.linalg.norm(np.subtract(p1, p2))

sz = (800, 600)

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20

    pts=[]
    centers=[]

    def init(numCenters):
        centers.clear()
        for i in range(numCenters):
            centers.append([
                np.random.randint(50, 750),
                np.random.randint(50, 550),
                0])
    def assign():
        for p in pts:
            dd=[dist(p[:2], c[:2]) for c in centers]
            p[2]=np.argmin(dd)
    def recalc():
        for i in range(len(centers)):
            pp=[p for p in pts if p[2]==i]
            if len(pp)>0:
                p=np.mean(pp, 0)
                centers[i]=p
    def runKMeans(numC):
        init(numC)
        for i in range(7):
            assign()
            recalc()
        assign()
    def calcError():
        res=0
        for c in centers:
            pp = [p for p in pts if p[2] == c[2]]
            dd=[dist(p[:2], c[:2]) for p in pp]
            e=np.sum(dd, 0)
            res+=e
        return res

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_l:
                    with open("pts2.txt", "r") as f:
                        pts=eval(f.read())
                        for i in range(len(pts)):
                            pts[i]=[*pts[i], 0]
                if ev.key == pygame.K_1:
                    init(3)
                if ev.key == pygame.K_2:
                    assign()
                if ev.key == pygame.K_3:
                    recalc()
                if ev.key == pygame.K_4:
                    runKMeans(7)
                if ev.key == pygame.K_5:
                    numCBest=1
                    # eBest=100500
                    ePrev=100500
                    centersBest=None
                    for numC in range(1, 12+1):
                        runKMeans(numC)
                        E=calcError()
                        print(f"Error (numC={numC}): {E}")
                        # if E<eBest:
                        #     eBest=E
                        #     numCBest=numC
                        #     print(f"Best num clusters: {numCBest}")
                        if ePrev-E<0:
                            numCBest=numC
                            centersBest=centers
                            print(f"Best num clusters (Elbow method): {numCBest}")
                            break
                        ePrev=E

                    centers=centersBest
                    assign()

        screen.fill((255, 255, 255))
        colors=[(255,0,0), (0,255,0), (0,0,255),
                (100,100, 0), (0,100,100), (100,0,100),
                (170, 0, 0), (0, 170, 0), (0, 0, 170),
                (50, 50, 0), (0, 50, 50), (50, 0, 50)
                ]

        if len(pts)>0:
            for p in pts:
                color=colors[p[2]]
                pygame.draw.circle(screen, color, p[:2], 5, 2)
            for c in centers:
                pygame.draw.circle(screen, (0,0,255), c[:2], 7, 1)

        drawText(screen, f"Test = {1}", 5, 5)

        pygame.display.flip()
        timer.tick(fps)

main()

#template file by S. Diane, RTU MIREA, 2024
