from classes import *
import random


def spawn_enemies(wave: int, enemy_bullet_speed: int) -> list:
    enemies = []
    for i in range(wave):
        enemy = Enemy(random.randrange(50, WIDTH - 100),
                      random.randrange(-1000, -50),
                      random.choice(['red', 'green', 'blue']),
                      enemy_bullet_speed)
        enemies.append(enemy)
    return enemies
