import sys, pygame
import numpy as np
import math

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
def drawText(screen, s, x, y):
    screen.blit(font.render(s, True, (0,0,0)), (x,y))

sz = (800, 600)

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
        dy=p[1]-(k*p[0]+b)
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
    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
        for i in range(10):
            gradDescent(0.1)
        screen.fill((255, 255, 255))
        for p in pts:
            pygame.draw.circle(screen, (0,0,0), p, 5, 2)
        drawLine(screen)
        mse=calcMSE()
        drawText(screen, f"MSE = {mse:.2f}", 5, 5)
        pygame.display.flip()
        timer.tick(20)

main()

#template file by S. Diane, RTU MIREA, 2024