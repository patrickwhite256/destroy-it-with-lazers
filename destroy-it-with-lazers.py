#!/usr/bin/env python

import os, pygame
from pygame.locals import *
from numpy import matrix
from numpy import linalg

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
            v = (-v[1], v[0])
            pmag = (direction[0] * v[0] + direction[1] * v[1])/(v[0]*v[0]+v[1]*v[1])
            proj = (v[0]*pmag,v[1]*pmag)
            direction = (direction[0]-2*proj[0],direction[1]-2*proj[1])
    return points

def main():
    pygame.init()
    pygame.display.set_caption("Destroy it with Lazers!")
    screen = pygame.display.set_mode((600, 600))
    startpos = None
    laserpath = None
    walls = []
    while True:
        ticks = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == MOUSEBUTTONDOWN:
                startpos = event.pos
            if event.type == MOUSEBUTTONUP:
                walls.append(LineSegment(startpos, event.pos))
                startpos = None
            if event.type == KEYDOWN:
                walls = []
        laserpath = computeLaserPath(walls + ([LineSegment(startpos, pygame.mouse.get_pos())] if startpos != None else []))

        screen.fill((200,200,200))
        for w in (walls):
            w.draw(screen, (0,0,255))
        if laserpath != None:
            pygame.draw.lines(screen, (255,0,0), False, laserpath)
        if startpos != None:
            pygame.draw.line(screen, (0,255,0),startpos, pygame.mouse.get_pos())

        while pygame.time.get_ticks() - ticks < 16:
            pass
        pygame.display.update()

if __name__ == '__main__': main()
