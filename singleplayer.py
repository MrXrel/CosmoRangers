import random

from classes import *
from images import BG, PLAYER_SHIP
from spawn_enemies import *
import pygame

pygame.font.init()

WIDTH = 700
HEIGHT = 900


def collide(bullet, ship) -> bool:
    """Return if objects overlap each other"""
    return bullet.mask.overlap(ship.mask, (ship.x - bullet.x, ship.y - bullet.y))


def main():
    pygame.init()
    pygame.display.set_caption('SinglePlayer')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    player = Player(300, 600, PLAYER_SHIP, 4, 1, (94, 100))
    running = True
    level = 0
    lives = 5
    wave = 3
    enemies = []
    enemy_bullets = []

    player_speed = 7
    enemy_speed = 1

    enemy_bullet_speed = -4

    main_font = pygame.font.SysFont('comicsans', 50)
    pause_font = pygame.font.SysFont('comicsans', 200)

    paused = False
    clock = pygame.time.Clock()

    def draw_screen():
        screen.blit(BG, (0, 0))
        lives_label = main_font.render(f'Жизни: {lives}', 1, (255, 255, 255))
        level_label = main_font.render(f'Уровень: {level}', 1, (255, 255, 255))
        # draw labels
        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        # draw enemies
        for enemy in enemies:
            enemy.update_sprite()
            enemy.draw(screen)
            enemy.reset_reload()

        # reset reload
        player.reset_reload()
        # refresh player sprite
        player.update_sprite()
        # draw bullets
        for b in player.bullets:
            b.update_sprite()
            b.draw(screen)

        # draw enemy bullets
        for b in enemy_bullets:
            b.update_sprite()
            b.draw(screen)

        # draw a player
        player.draw(screen)
        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        pygame.display.update()

    while running:
        # TODO end of the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    paused = not paused
        if not paused:
            if len(enemies) == 0:
                level += 1
                wave += 4
                # spawn enemies
                enemies = spawn_enemies(wave, enemy_bullet_speed)

            # get all pressed keys
            key_pressed = pygame.key.get_pressed()
            # up
            if key_pressed[pygame.K_w] and player.get_height() + player_speed - 5 >= 0:
                player.y -= player_speed
            # down
            if key_pressed[pygame.K_s] and player.get_height() + player_speed + player.img.get_height() <= HEIGHT:
                player.y += player_speed
            # left
            if key_pressed[pygame.K_a] and player.get_width() + player_speed - 5 >= 0:
                player.x -= player_speed
            # right
            if key_pressed[pygame.K_d] and player.get_width() + player_speed + player.img.get_width() <= WIDTH:
                player.x += player_speed

            # if key_pressed[pygame.K_SPACE]:
            #     if level >= 10:
            #         player.advanced_shoot()
            #     else:
            #         player.shoot()

            if level >= 15:
                player.advanced_shoot(size=(20, 55))
            else:
                player.shoot(size=(20, 55))

            # move bullets
            for b in player.bullets[:]:
                b.move()
                # check if bullets is out of the screen
                if b.y + b.img.get_height() <= 0:
                    player.bullets.remove(b)

            # move enemy bullets
            for b in enemy_bullets[:]:
                b.move()
                # if bullet catch the player
                if collide(b, player):
                    enemy_bullets.remove(b)
                    lives -= 1
                # delete bullet if it's out of the screen
                if b.y - b.img.get_height() >= HEIGHT:
                    enemy_bullets.remove(b)

            # check if bullet catch the enemy
            for enemy in enemies[:]:
                for b in player.bullets[:]:
                    # if catch
                    if collide(b, enemy):
                        try:
                            enemies.remove(enemy)
                            player.bullets.remove(b)
                        except ValueError:
                            pass
                # check if enemy touch the player
                if collide(enemy, player):
                    try:
                        enemies.remove(enemy)
                        lives -= 1
                    except ValueError:
                        pass

            # move enemies
            for e in enemies[:]:
                e.move(enemy_speed)
                # check if they touch the screen
                if e.y + e.img.get_height() >= HEIGHT:
                    enemies.remove(e)
                    lives -= 1
                # shoot
                if not random.randrange(0, 1000):
                    e.shoot_(enemy_bullets)
            draw_screen()
            clock.tick(60)
        elif paused:
            pause_label = pause_font.render('Пауза', 1, (255, 255, 255))
            screen.blit(pause_label, (WIDTH // 2 - pause_label.get_width() // 2, HEIGHT // 2 - pause_label.get_height() // 2))
            pygame.display.update()
    pygame.quit()
    from CosmoRangers import start
    start(1)


if __name__ == '__main__':
    main()
