import pygame
import os

WIDTH = 700
HEIGHT = 900

# background
BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background-black.png')), (WIDTH, HEIGHT))

# ships
PLAYER_SHIP = pygame.image.load(os.path.join('Assets', 'Ships', 'Flying', 'PLAYERSHIP1.png'))

# enemy ships
RED_BIG_SHIP = pygame.image.load(os.path.join('Assets', 'Ships', 'Flying', 'REDVOYAGERSHEET1.png'))
BLUE_BIG_SHIP = pygame.image.load(os.path.join('Assets', 'Ships', 'Flying', 'BLUEVOYAGERSHEET1.png'))
RED_MID_SHIP = pygame.image.load(os.path.join('Assets', 'Ships', 'Flying', 'REDMANTASHEET1.png'))
BLUE_MID_SHIP = pygame.image.load(os.path.join('Assets', 'Ships', 'Flying', 'BLUEMANTASHEET1.png'))
PURPLE_MID_SHIP = pygame.image.load(os.path.join('Assets', 'Ships', 'Flying', 'PURPLEMANTASHEET1.png'))
PURPLE_SMALL_SHIP = pygame.image.load(os.path.join('Assets', 'Ships', 'Flying', 'PURPLEFALCONSHEET1.png'))
BLUE_SMALL_SHIP = pygame.image.load(os.path.join('Assets', 'Ships', 'Flying', 'BLUEFALCONSHEET1.png'))
RED_SMALL_SHIP = pygame.image.load(os.path.join('Assets', 'Ships', 'Flying', 'REDFALCONSHEET1.png'))

# Bullets
BLUE_BULLET = pygame.image.load(os.path.join('Assets', 'projectiles', 'rockets', 'BLUESMALLROCKET1.png'))
RED_BULLET = pygame.image.load(os.path.join('Assets', 'projectiles', 'rockets', 'REDSMALLROCKET1.png'))
PURPLE_BULLET = pygame.image.load(os.path.join('Assets', 'projectiles', 'rockets', 'PURPLESMALLROCKET1.png'))
YELLOW_BULLET = pygame.image.load(os.path.join('Assets', 'projectiles', 'rockets', 'WHITEBIGROCKET1.png'))