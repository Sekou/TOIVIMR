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


pts=[
    [200, 200],
    [250, 260],
    [300, 300],
    [350, 360],
    [400, 420],
    [450, 490]
]

k=0.7
b=100
def drawLine(screen):
    p1=[0, k*0+b]
    p2=[800, k*800+b]
    pygame.draw.line(screen, (0,255,0), p1, p2, 2)

def calcMSE():
    res=0
    for p in pts:
        dy=p[0]-(k*p[0]+b)
        res+=dy*dy
    return res/len(pts)

def gradDescent(eta):
    global k, b
    dEdk, dEdb = 0, 0
    for p in pts:
        dEdk += p[0]*(k*p[0] + b - p[1])
        dEdb += (k * p[0] + b - p[1])
    k-=eta*dEdk/len(pts)/10000
    b-=eta*dEdb/len(pts)/100

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1:
                    gradDescent(0.1)


        for i in range(10):
            gradDescent(0.1)

        dt=1/fps

        screen.fill((255, 255, 255))

        for p in pts:
            pygame.draw.circle(screen, (0,0,0), p, 5, 2)
        drawLine(screen)

        mse=calcMSE()
        drawText(screen, f"MSE = {mse}", 5, 5)

        pygame.display.flip()
        timer.tick(fps)

main()

#template file by S. Diane, RTU MIREA, 2024