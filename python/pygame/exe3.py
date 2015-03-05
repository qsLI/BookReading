#coding=utf-8
import pygame
from pygame.locals import *
from sys import exit

pygame.init()
backgroundImg = r"C:\Users\KL\Pictures\Dengge.gif"
SCREEN_SIZE = (640,480)
screen = pygame.display.set_mode(SCREEN_SIZE,RESIZABLE,32)
backgroud = pygame.image.load(backgroundImg).convert()

x,y = 0,0
move_x,move_y = 0,0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == VIDEORESIZE:
            SCREEN_SIZE = event.size
            print dir(screen)
            screen = pygame.display.set_mode(SCREEN_SIZE,RESIZABLE,32)
            pygame.display.set_caption("Windows resized to " + str(event.size))

            screenWidth,screenHeight = SCREEN_SIZE
            for y in range(0,screenHeight,backgroud.get_height()):
                for x in range(0,screenWidth,backgroud.get_width()):
                    screen.blit(backgroud,(x,y))
            pygame.display.update()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                move_x = -1
            elif event.key == K_RIGHT:
                move_x = 1
            elif event.key == K_UP:
                move_y = -1
            elif event.key == K_DOWN:
                move_y = 1
        elif event.type == KEYUP:
            move_x = 0
            move_y = 0
            
        x += move_x
        y += move_y
        
        screen.fill((0,0,0))
        screen.blit(backgroud,(x,y))
        
        pygame.display.update()
                
            