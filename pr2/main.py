import sys, pygame
import numpy as np
import math

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
def drawText(screen, s, x, y):
    surf=font.render(s, True, (0,0,0))
    screen.blit(surf, (x,y))

sz = (800, 600)

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20

    pts=[]

    rdpPts=[0]

    def ptSegmDist(p, p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        if dx == 0: dx = 0.0000001
        k = dy / dx
        b = p1[1] - k * p1[0]
        return np.abs(-k * p[0] + p[1] - b) / math.sqrt(k * k + 1)

    def selectRDPPoint(i1, eps):
        i2=-1
        for i in range(i1+1, len(pts)): #цикл по выбору опорной точки
            for j in range(i1+1, i): #цикл проверки близости точек данных
                d=ptSegmDist(pts[j], pts[i1], pts[i])
                if d>eps:
                    i2=i-1
                    break
            if i2>=0:
                break
            if i==len(pts)-1 and i2<0:
                i2=i
        return i2

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_l:
                    with open("pts2.txt", "r") as f:
                        pts=eval(f.read())
                if ev.key == pygame.K_1:
                    iLast=rdpPts[-1]
                    i=selectRDPPoint(iLast, 15)
                    rdpPts.append(i)
                    print("rdp i: ", i)

        dt=1/fps

        screen.fill((255, 255, 255))
        if len(pts)>0:
            for p in pts:
                pygame.draw.circle(screen, (255,0,0), p, 5, 2)
            for i in rdpPts:
                pygame.draw.circle(screen, (0,0,255), pts[i], 7, 1)
            if len(rdpPts)>=2:
                for i in range(len(rdpPts)-1):
                    i1,i2=rdpPts[i], rdpPts[i+1]
                    pygame.draw.line(screen, (0, 0, 255), pts[i1], pts[i2], 2)

        drawText(screen, f"Test = {1}", 5, 5)

        pygame.display.flip()
        timer.tick(fps)

main()

#template file by S. Diane, RTU MIREA, 2024
