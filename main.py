import pygame
from missileGame import playGame
from gameOver import DieUser
from user import User

swidth, sheight = 500, 700  # 화면 크기

# part of main code
pygame.init()
monitor = pygame.display.set_mode((swidth, sheight))
pygame.display.set_caption('우주괴물 무찌르기')
user = User(pygame)

while True:
    playGame(monitor, pygame, swidth, sheight, user)
    DieUser(monitor, pygame, sheight)
