import pygame
from missileGame import playGame
from user import User
from monitor import Monitor
import sys


# part of main code
pygame.init()

monitor = Monitor(pygame)
user = User(pygame)

while True:
    if user.userState == 'live':
        playGame(monitor, pygame, user)
    elif user.userState == 'die':
        user.dieUser(monitor, pygame)
    elif user.userState == 'quit':
        sys.exit()