#!/usr/bin/env python

import os, pygame
from pygame.locals import *
from numpy import matrix
from numpy import linalg

NUMSTATES = 3
class GameRect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 0
        self.wall = None
    def draw(self, display):
        border = (0,0,0)
        fill = (200,200,200)
        line = (0,255,0)
        pygame.draw.rect(display, fill, (self.x * 40, self.y * 40, 40, 40), 0)
        if self.state == 0:
            self.wall = None
            pass
        elif self.state == 1:
            self.wall = LineSegment((self.x * 40, self.y * 40), ((self.x + 1) * 40, (self.y + 1) * 40))
        elif self.state == 2:
            self.wall = LineSegment((self.x * 40, (self.y + 1) * 40), ((self.x + 1) * 40, self.y * 40))
        if self.wall != None:
            self.wall.draw(display,line)
        pygame.draw.rect(display, border, (self.x * 40, self.y * 40, 40, 40), 1)
    def contains(self, pos):
        if pos[0] > self.x * 40 and pos[0] < (self.x + 1) * 40 and pos[1] > self.y * 40 and pos[1] < (self.y + 1) * 40:
            return True
        return False
    def shift(self):
        self.state = (self.state + 1) % NUMSTATES

class Line:
    def __init__(self, pos, dirvec):
        self.pos = pos
        self.dirvec = dirvec
    def intersects(self, line):
        A = matrix([[self.dirvec[0],-line.dirvec[0]],[self.dirvec[1],-line.dirvec[1]]])
        if(linalg.det(A) == 0):
            return None
        x = matrix([[line.pos[0] - self.pos[0]],[line.pos[1] - self.pos[1]]])
        return linalg.solve(A,x).A1
    def at(self, t):
        return (self.pos[0] + self.dirvec[0] * t, self.pos[1] + self.dirvec[1] * t)

class LineSegment:
    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2
        self.line = Line(pos1,(pos2[0]-pos1[0],pos2[1]-pos1[1]))
    def intersects(self, line):
        intersection = self.line.intersects(line)
        if intersection == None:
            return None
        t = intersection[0]
        if t < 0 or t > 1:
            return None
        return intersection[1]
    def draw(self, display, color):
        pygame.draw.line(display, color, self.pos1, self.pos2)

def computeLaserPath(walls):
    points = [(0,20)]
    direction = (1,0)
    lastWall = None
    while True:
        currentWall = None
        laserLine = Line(points[len(points) - 1], direction)
        minIntersection = None
        for w in walls:
            if w == lastWall:
                continue
            intersection = w.intersects(laserLine)
            if intersection != None and intersection > 0:
                if minIntersection == None or intersection < minIntersection:
                    minIntersection = intersection
                    currentWall = w
        if minIntersection == None:
            points.append(laserLine.at(1000))
            break
        else:
            points.append(laserLine.at(minIntersection))
            lastWall = currentWall
            v = currentWall.line.dirvec
            v = (v[1], v[0])
            pmag = (direction[0] * v[0] + direction[1] * v[1])/(v[0]*v[0]+v[1]*v[1])
            proj = (v[0]*pmag,v[1]*pmag)
            direction = (2*proj[0]-direction[0],2*proj[1]-direction[1])
            print("new dir:", direction)
    return points

def main():
    pygame.init()
    pygame.display.set_caption("Destroy it with Lazers!")
    screen = pygame.display.set_mode((240, 240))
    rects = []
    for i in range(36):
        r = GameRect(i % 6, int(i / 6))
        rects.append(r)
    lasermoving = False

    laserpath = None
    while True:
        ticks = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == MOUSEBUTTONDOWN:
                for r in rects:
                    if r.contains(event.pos):
                        r.shift()
            if event.type == KEYDOWN:
                lasermoving = True
                walls = []
                for r in rects:
                    if r.wall != None:
                        walls.append(r.wall)
                laserpath = computeLaserPath(walls)
                print(laserpath)

        screen.fill((255,255,255))
        for r in rects:
            r.draw(screen)
        if laserpath != None:
            pygame.draw.lines(screen, (255,0,0), False, laserpath)

        while pygame.time.get_ticks() - ticks < 16:
            pass
        pygame.display.update()

if __name__ == '__main__': main()
