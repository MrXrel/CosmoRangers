import os
import random

import pygame

pygame.font.init()

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


class Bullet:
    def __init__(self, x, y, img, speed=4):
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.y -= self.speed

    # def collide_with(self, other):
    #     return self.img.get_rect().colliderect(other.img.get_rect())


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.img = None
        self.bullet_img = None
        # bullets which were shot by this ship

        self.bullets = []
        self.damage = 20
        self.reload = 0

    def draw(self, screen):
        # draw a ship
        screen.blit(self.img, (self.x, self.y))

    def shoot(self):
        if self.reload == 0:
            bullet = Bullet(self.x, self.y - self.img.get_height() + 20, self.bullet_img)
            self.bullets.append(bullet)
            self.reload = 1

    def reset_reload(self):
        # if there is a reload add one every frame
        if self.reload != 0:
            self.reload += 1
        # if reload > 30, it half a second has passed
        if self.reload > 25:
            self.reload = 0

    def get_height(self):
        return self.y

    def get_width(self):
        return self.x

    # def collide_with(self, other):
    #     return self.img.get_rect().colliderect(other.img.get_rect())


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.img = PLAYER_SHIP
        self.bullet_img = YELLOW_BULLET
        self.mask = pygame.mask.from_surface(self.img)

    def advanced_shoot(self):
        if self.reload == 0:
            bullet = Bullet(self.x + 10, self.y - self.img.get_height() + 20, self.bullet_img)
            bullet2 = Bullet(self.x - 10, self.y - self.img.get_height() + 20, self.bullet_img)
            self.bullets.append(bullet)
            self.bullets.append(bullet2)
            self.reload = 1


class Enemy(Ship):
    types_of_ships = {
        'red': [RED_SHIP, RED_BULLET],
        'blue': [BLUE_SHIP, BLUE_BULLET],
        'green': [GREEN_SHIP, GREEN_BULLET]

    }

    def __init__(self, x, y, color, bullet_speed, health=100):
        super().__init__(x, y, health)
        ship = self.types_of_ships[color]
        self.img = ship[0]
        self.bullet_img = ship[1]
        self.speed = bullet_speed
        self.mask = pygame.mask.from_surface(self.img)

    def move(self, speed: int):
        self.y += speed

    def shoot_(self, enemy_bullets: list):
        # check if enemy is on the screen
        if self.y + self.img.get_height() >= 1:
            if self.reload == 0:
                bullet = Bullet(self.x, self.y - self.img.get_height() + 20, self.bullet_img, self.speed)
                enemy_bullets.append(bullet)
                self.reload = 1

    def reset_reload(self):
        # if there is a reload add one every frame
        if self.reload != 0:
            self.reload += 1
        # if reload > 30, it half a second has passed
        if self.reload > 70:
            self.reload = 0


def collide(bullet, ship) -> bool:
    """Return if objects overlap each other"""
    return bullet.mask.overlap(ship.mask, (ship.x - bullet.x, ship.y - bullet.y))


def main():
    pygame.init()
    pygame.display.set_caption('SinglePlayer')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    player = Player(300, 600)
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
            enemy.draw(screen)
            enemy.reset_reload()

        # reset reload
        player.reset_reload()
        # draw bullets
        for b in player.bullets:
            b.draw(screen)

        # draw enemy bullets
        for b in enemy_bullets:
            b.draw(screen)

        # draw a player
        player.draw(screen)

        pygame.display.update()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if len(enemies) == 0:
            level += 1
            wave += 4
            for i in range(wave):
                enemy = Enemy(random.randrange(50, WIDTH - 100),
                              random.randrange(-1000, -50),
                              random.choice(['red', 'green', 'blue']),
                              enemy_bullet_speed)
                enemies.append(enemy)

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

        if level >= 10:
            player.advanced_shoot()
        else:
            player.shoot()

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
            # if out of the screen
            if b.y - b.img.get_height() >= HEIGHT:
                print('b')
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
    pygame.quit()


if __name__ == '__main__':
    main()
