import math
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos

kpi=np.pi/180

def drawPoints(pts):
    glPointSize(3)
    glBegin(GL_POINTS)
    for p in pts:
        glVertex3fv(p)
    glEnd()

def drawAxes():
    for v in np.array(((1,0,0),(0,1,0),(0,0,1))):
        glColor(v)
        glBegin(GL_LINES)
        glVertex3fv((0,0,0))
        glVertex3fv(v)
        glEnd()

def rotate(pts, r, p, y):
    cr, cp, cy = cos(r), cos(p), cos(y)
    sr, sp, sy = sin(r), sin(p), sin(y)
    myaw = [[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]]  # z
    mpit = [[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]]  # y
    mrol = [[1, 0, 0], [0, cr, -sr], [0, sr, cr]]  # x
    mat = np.array(myaw) @ mpit @ mrol
    res = mat.dot(np.transpose(pts))
    res = np.transpose(res)
    return res

#первое облако
pts=[
    [0.5,0.3,0.4],
    [0.2,0.3,0.4],
    [0.5,0.7,0.4],
    [0.5,0.3,0.6],
    [0.5,0.5,0.5]
]
#второе облако
pts2 = rotate(pts, 45*kpi, 0, 0)
pts2 = pts2 + [0.5,0.3,0.1]

def calcAxisAngle(c, pts, pts2):
    vsum=np.zeros(3)
    asum, cnt = 0, 0
    for p in pts:
        #ищем ближайшую точку
        dd = [np.linalg.norm(np.subtract(p, p2)) for p2 in pts2]
        i = np.argmin(dd)
        nb = pts2[i]
        #вычисляем угол
        v1 = np.subtract(p, c)
        v2 = np.subtract(nb, c)
        z=np.cross(v1, v2)
        if np.linalg.norm(z)>0:
            z/=np.linalg.norm(z) #ось вращения
            cosang=np.dot(v1, v2)/np.linalg.norm(v1)/np.linalg.norm(v2)
            if 0<cosang<1:
                ang = math.acos(cosang) #угол вращения
                vsum+=z
                asum+=ang
                cnt+=1
    return vsum/np.linalg.norm(vsum), asum/cnt

def getRotMat(axis, angle):
    x,y,z=axis
    c, s = math.cos(angle), math.sin(angle)
    c_=1-c
    M=[[c+x*x*c_, x*y*c_-z*s, x*z*c_+y*s],
       [y*x*c_+z*s, c+y*y*c_, y*z*c_-x*s],
       [z*x*c_-y*s, z*y*c_+x*s, c+z*z*c_]]
    return np.array(M)

def main():
    global pts, pts2
    pygame.init()
    display=(800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0,0,-3)

    TR = np.zeros(3)
    R = np.zeros(3)

    #разворот системы координат, чтоб ось Z была направлена вверх
    glMultMatrixf([ [0,0,-1,0],[-1,0,0,0],[0,1,0,0],[0,0,0,1] ])
    glTranslatef(0,0,-0.5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key==K_1:
                    c1=np.mean(pts, axis=0)
                    c2=np.mean(pts2, axis=0)
                    TR=c1-c2
                    pts2=[p + TR for p in pts2]
                if event.key==K_2:
                    c = np.mean(pts, axis=0) #общий центр совмещенных облаков
                    v,a=calcAxisAngle(c1, pts, pts2)
                    R=getRotMat(v, -a)
                    pts2 = [p - c for p in pts2]
                    pts2=np.transpose(R.dot(np.transpose(pts2)))
                    pts2 = [p + c for p in pts2]

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(1, 1, 1, 1)

        glRotate(1, 0,0,1) #поворот на 1 градус вокруг оси Z
        drawAxes()

        glColor((1,0,0))
        drawPoints(pts)
        glColor((0,0,1))
        drawPoints(pts2)

        pygame.display.flip()
        pygame.time.wait(50)

main()

#template file by S. Diane, RTU MIREA, 2024
