import itertools
import sys, pygame
import numpy as np

colors = [[0, 255, 0], [255, 0, 255], [0, 127, 255],
          [255, 127, 0], [127, 191, 127], [106,42, 137],
          [ 75, 118, 2], [213, 0, 9], [227, 127, 252], [0, 0, 255]]
sz = (800, 600)

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
def drawText(screen, s, x, y):
    surf=font.render(s, True, (0,0,0))
    screen.blit(surf, (x,y))

#робот в виде оси графика
class Axis:
    def __init__(self, id, x, y, lx, ly):
        self.id, self.x, self.y, self.lx, self.ly=id, x, y, lx, ly
        self.taskIds=[]
    def draw(self, screen, tasks):
        dx, kt, h, gap = 20, 2, 25, 7
        pygame.draw.line(screen, (0,0,0), [self.x, self.y], [self.x+self.lx, self.y], 2)
        pygame.draw.line(screen, (0,0,0), [self.x, self.y], [self.x, self.y-self.ly], 2)
        drawText(screen, f"{self.id}", self.x-20, self.y-self.ly)
        for i in range(1, self.lx//dx - 1):
            pygame.draw.line(screen, (0, 0, 0),
                             [self.x+i*dx, self.y-3], [self.x+i*dx, self.y + 3], 1)
        shift=0
        for i in self.taskIds:
            t=tasks[i]*kt
            pygame.draw.rect(screen, colors[i], [self.x+shift+gap/2, self.y-h-5, t-gap/2, h], 0)
            drawText(screen, f"{i}", self.x+shift+t/2-10, self.y-self.ly*0.83)
            shift+=t

    def getTotalTime(self, tasks):
        return sum(tasks[i] for i in self.taskIds)

def getPartitions(lst, numGroups, recursionLevel=0):
    if len(lst)==0:  # если список пустой, вернуть пустой список
        return [[]]
    result = []
    # проходим по всем величинам групп
    for i in range(1, len(lst) + 1):
        # получаем текущую группу элементов
        for group in itertools.combinations(lst, i):
            remaining = [x for x in lst if x not in group]  # оставшиеся элементы
            for p in getPartitions(remaining, -1, recursionLevel+1):  # рекурсивное разбиение
                tmpResult=[list(group)] + p
                if recursionLevel==0 and numGroups>0 and len(tmpResult)!=numGroups:
                    continue
                result.append(tmpResult)
    return result

def calcTime(tasks, axes):
    maxt=max(a.getTotalTime(tasks) for a in axes)
    return maxt

def getBestPartition(axes, tasks):
    ii = np.arange(len(tasks))
    pp = getPartitions(ii, len(axes), 0)
    bestT=100500
    bestPartition=None
    for p in pp:
        for i in range(len(axes)):
            axes[i].taskIds = p[i]
        t = calcTime(tasks, axes)
        if t<bestT:
            bestT=t
            bestPartition=p
    return bestPartition, bestT

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

    t=calcTime(tasks, axes)
    print("Initial time: ", t)

    bestPartition, bestT = getBestPartition(axes, tasks)

    print("Best time: ", bestT)
    print("Best partition: ", bestPartition)
    for i in range(len(axes)):
        axes[i].taskIds = bestPartition[i]

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    print("Hi")

        screen.fill((255, 255, 255))

        for a in axes:
            a.draw(screen, tasks)

        pygame.display.flip()
        timer.tick(fps)

main()

#template file by S. Diane, RTU MIREA, 2024