import pygame
import os

WIDTH = 700
HEIGHT = 900

# pictures
BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background-black.png')), (WIDTH, HEIGHT))

# ships
PLAYER_SHIP = pygame.image.load(os.path.join('Assets', 'pixel_ship_yellow.png'))
# enemy ships
BLUE_SHIP = pygame.image.load(os.path.join('Assets', 'pixel_ship_blue_small.png'))
RED_SHIP = pygame.image.load(os.path.join('Assets', 'pixel_ship_red_small.png'))
GREEN_SHIP = pygame.image.load(os.path.join('Assets', 'pixel_ship_green_small.png'))

# Bullets
YELLOW_BULLET = pygame.image.load(os.path.join('Assets', 'pixel_laser_yellow.png'))
BLUE_BULLET = pygame.image.load(os.path.join('Assets', 'pixel_laser_blue.png'))
RED_BULLET = pygame.image.load(os.path.join('Assets', 'pixel_laser_red.png'))
GREEN_BULLET = pygame.image.load(os.path.join('Assets', 'pixel_laser_green.png'))