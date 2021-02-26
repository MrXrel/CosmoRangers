import pygame
import os

WIDTH = 700
HEIGHT = 900

# pictures
BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background-black.png')), (WIDTH, HEIGHT))

# ships
PLAYER_SHIP = pygame.image.load(os.path.join('Assets', 'Ships', 'Flying', 'PLAYERSHIP1.png'))
# enemy ships
RED_BIG_SHIP = pygame.image.load(os.path.join('Assets', 'Ships', 'Flying', 'REDVOYAGERSHEET1.png'))
BLUE_BIG_SHIP = pygame.image.load(os.path.join('Assets', 'Ships', 'Flying', 'BLUEVOYAGERSHEET1.png'))
PURPLE_SMALL_SHIP = pygame.image.load(os.path.join('Assets', 'Ships', 'Flying', 'PURPLEFALCONSHEET1.png'))
BLUE_SMALL_SHIP = pygame.image.load(os.path.join('Assets', 'Ships', 'Flying', 'BLUEFALCONSHEET1.png'))
RED_SMALL_SHIP = pygame.image.load(os.path.join('Assets', 'Ships', 'Flying', 'REDFALCONSHEET1.png'))
# Bullets
YELLOW_BULLET = pygame.image.load(os.path.join('Assets', 'pixel_laser_yellow.png'))
BLUE_BULLET = pygame.image.load(os.path.join('Assets', 'pixel_laser_blue.png'))
RED_BULLET = pygame.image.load(os.path.join('Assets', 'pixel_laser_red.png'))
GREEN_BULLET = pygame.image.load(os.path.join('Assets', 'pixel_laser_green.png'))