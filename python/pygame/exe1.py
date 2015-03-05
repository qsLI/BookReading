#coding=utf-8
import pygame
from pygame.locals import *
from sys  import exit

backgroudImg = r"C:\Users\KL\Pictures\22.jpg"
mouseImg = r"C:\Users\KL\Pictures\2.jpg"

pygame.init()

screen = pygame.display.set_mode((1920,1080),0,32)
pygame.display.set_caption("Hello Garfield!")

backgroud = pygame.image.load(backgroudImg).convert()
mouseCursor = pygame.image.load(mouseImg).convert_alpha()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        screen.blit(backgroud,(0,0))
        
        x,y = pygame.mouse.get_pos()
        
        x -= mouseCursor.get_width()/2
        y -= mouseCursor.get_height()/2
        
        screen.blit(mouseCursor,(x,y))
        pygame.display.update()