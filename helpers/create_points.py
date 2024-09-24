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

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20

    pts=[]

    def findNearestPt(pos, thr):
        dd=[dist(p, pos) for p in pts]
        i=np.argmin(dd)
        if dd[i]<thr:
            return pts[i]
        return None

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_s:
                    with open("pts.txt", "w") as f:
                        f.write(str(pts))
                if ev.key == pygame.K_l:
                    with open("pts.txt", "r") as f:
                        pts=eval(f.read())
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 3:
                    p=findNearestPt(ev.pos, 15)
                    if p in pts:
                        pts.remove(p)
                else: pts.append(ev.pos)


        dt=1/fps

        screen.fill((255, 255, 255))
        for p in pts:
            pygame.draw.circle(screen, (255,0,0), p, 5, 2)

        drawText(screen, f"Test = {1}", 5, 5)

        pygame.display.flip()
        timer.tick(fps)

main()

#template file by S. Diane, RTU MIREA, 2024
