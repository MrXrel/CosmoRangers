import os

import pygame
pygame.font.init()


WIDTH = 700
HEIGHT = 900

# pictures
BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background-black.png')), (WIDTH, HEIGHT))

# ships
PLAYER_SHIP = pygame.image.load(os.path.join('Assets', 'pixel_ship_yellow.png'))

# Bullets
YELLOW_BULLET = pygame.image.load(os.path.join('Assets', 'pixel_laser_yellow.png'))


class Bullet:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.speed = 4

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.y -= self.speed


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
        if self.reload > 30:
            self.reload = 0

    def get_height(self):
        return self.y

    def get_width(self):
        return self.x


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.img = PLAYER_SHIP
        self.bullet_img = YELLOW_BULLET


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    player = Player(300, 600)
    running = True
    level = 1
    lives = 5
    player_speed = 7
    main_font = pygame.font.SysFont('comicsans', 50)

    clock = pygame.time.Clock()

    def draw_screen():
        screen.blit(BG, (0, 0))
        lives_label = main_font.render(f'Жизни: {lives}', 1, (255, 255, 255))
        level_label = main_font.render(f'Уровень: {level}', 1, (255, 255, 255))

        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        player.reset_reload()
        for b in player.bullets:
            b.draw(screen)
        player.draw(screen)

        pygame.display.update()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        if key_pressed[pygame.K_SPACE]:
            player.shoot()

        for b in player.bullets:
            b.move()
        draw_screen()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
