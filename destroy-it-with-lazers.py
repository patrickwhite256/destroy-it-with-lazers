#!/usr/bin/env python

import os, pygame
from pygame.locals import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((240, 240))


    while 1:
        ticks = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                return


        pygame.display.update()
        while pygame.time.get_ticks() - ticks < 16:
            pass



if __name__ == '__main__': main()
