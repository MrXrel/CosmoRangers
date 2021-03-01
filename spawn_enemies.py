from classes import *
import random
from images import *


def spawn_enemies(wave: int, enemy_bullet_speed: int) -> list:
    enemies = []
    types_of_ships = {
        'red_big': [RED_BIG_SHIP, RED_BULLET, (50, 67)],
        'blue_big': [BLUE_BIG_SHIP, BLUE_BULLET, (50, 67)],
        'purple_small': [PURPLE_SMALL_SHIP, PURPLE_BULLET, (94, 100)],
        'blue_small': [BLUE_SMALL_SHIP, BLUE_BULLET, (94, 100)],
        'red_small': [RED_SMALL_SHIP, RED_BULLET, (94, 100)],
        'red_mid': [RED_MID_SHIP, RED_BULLET, (94, 57)],
        'blue_mid': [BLUE_MID_SHIP, BLUE_BULLET, (94, 57)],
        'purple_mid': [PURPLE_MID_SHIP, PURPLE_BULLET, (94, 57)]

    }
    for i in range(wave):
        ship = types_of_ships[random.choice(list(types_of_ships.keys()))]
        enemy = Enemy(random.randrange(50, WIDTH - 100),
                      random.randrange(-1000, -50),
                      enemy_bullet_speed, ship, 4, 1, ship[2])
        enemies.append(enemy)
    return enemies

