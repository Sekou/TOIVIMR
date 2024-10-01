import itertools
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

class Axis:
    def __init__(self, id, x, y, lx, ly):
        self.id, self.x, self.y, self.lx, self.ly=id, x, y, lx, ly
        self.taskIds=[]
    def draw(self, screen, tasks):
        pygame.draw.line(screen, (0,0,0), [self.x, self.y], [self.x+self.lx, self.y], 2)
        pygame.draw.line(screen, (0,0,0), [self.x, self.y], [self.x, self.y-self.ly], 2)
        drawText(screen, f"{self.id}", self.x-20, self.y-20)

        gap=5
        h = 25
        shift=gap
        for i in self.taskIds:
            t=tasks[i]
            pygame.draw.rect(screen, (0,0,255), [self.x+shift, self.y-h-5, t, h], 0)
            shift+=t+gap

    def getTotalTime(self, tasks):
        return sum(tasks[i] for i in self.taskIds)

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


# def partitions(lst):
#     if len(lst)==0:
#         return [[]]
#     result = []
#     for i in range(1, len(lst) + 1):
#         for c in itertools.combinations(lst, i):
#             remaining = [x for x in lst if x not in c]
#             for p in partitions(remaining):
#                 result.append([list(c)] + p)
#     return result


def partitions(lst, numGroups, level=0):
    if len(lst)==0:  # Базовый случай: если список пустой, вернуть пустой список
        return [[]]
    result = []
    # Проходим по всем индексам и выбираем из начального элемента
    for i in range(1, len(lst) + 1):
        # Получаем текущую группу элементов
        for combo in itertools.combinations(lst, i):
            remaining = [x for x in lst if x not in combo]  # Оставшиеся элементы
            for p in partitions(remaining, -1, level+1):  # Рекурсивно разбиение оставшихся
                tmpResult=[list(combo)] + p
                if numGroups>0 and level==0 and len(tmpResult)!=numGroups:
                    continue
                result.append(tmpResult)
    return result

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20

    tasks=[10, 30, 20, 70, 40, 50]

    axes=[
        Axis(2, 100,200,300,70),
        Axis(1, 100,270,300,70),
        Axis(0, 100,340,300,70)
    ]

    axes[0].taskIds=[0,1]
    axes[1].taskIds=[2,3]
    axes[2].taskIds=[4,5]

    def calcTime(tasks, axes):
        maxt=max(a.getTotalTime(tasks) for a in axes)
        return maxt

    t=calcTime(tasks, axes)
    print(t)

    ii=np.arange(len(tasks))
    pp=partitions(ii, len(axes), 0)
    print(pp)

    bestT=100500
    bestPartition=None
    for p in pp:
        for i in range(len(axes)):
            axes[i].taskIds = p[i]
        t = calcTime(tasks, axes)
        if t<bestT:
            bestT=t
            bestPartition=p

    print("Best time: ", t)
    print("Best partition: ", bestPartition)
    for i in range(len(axes)):
        axes[i].taskIds = bestPartition[i]

    # inds=np.arange(len(tasks))
    # combinations = itertools.combinations

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    print("Hi")

        dt=1/fps

        screen.fill((255, 255, 255))

        for a in axes:
            a.draw(screen, tasks)

        drawText(screen, f"Test = {1}", 5, 5)

        pygame.display.flip()
        timer.tick(fps)

main()

#template file by S. Diane, RTU MIREA, 2024