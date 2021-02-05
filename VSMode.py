#  Created by X-Corporation


import os
import sys

import pygame

pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("VS Mode Test")
background = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background-black.png')), (width, height))


def load_image(name, colorkey=None):
    fullname = os.path.join('Assets', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


all_sprites = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y, num):
        super().__init__(all_sprites)
        self.image = load_image(image)
        self.x = x
        self.y = y
        self.health = 200
        self.bullets = []
        self.damage = 20
        self.reload = 0
        self.image = pygame.transform.scale(self.image, [67, 55])
        self.rect = self.image.get_rect()
        if num == 1:
            self.rect.topleft = self.x, self.y
            self.laserim = load_image('pixel_laser_yellow.png')
            self.image = pygame.transform.rotate(self.image, 90)
        elif num == 2:
            self.rect.topright = self.x, self.y
            self.image = pygame.transform.rotate(self.image, 270)

    def update(self, x, y, num):
        self.x = self.x + x
        self.y = self.y + y
        if num == 1:
            self.rect.topleft = self.x, self.y
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.y = self.y - y
                self.rect.topleft = self.x, self.y
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.x = self.x - x
                self.rect.topleft = self.x, self.y
        elif num == 2:
            self.rect.topright = self.x, self.y
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.y = self.y - y
                self.rect.topright = self.x, self.y
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.x = self.x - x
                self.rect.topright = self.x, self.y

    def shoot(self):
        if self.reload == 0:
            bullet = Bullet(self.x, self.y - self.image.get_height() + 20, self.laserim)
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


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
            self.image.set_colorkey(pygame.Color('cyan'))

        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


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


def vs():
    global horizontal_borders
    global vertical_borders
    player1 = Player('spaceship_yellow.png', 0, height / 2, 1)
    player2 = Player('spaceship_red.png', width, height // 2, 2)
    all_sprites.add(player1)
    all_sprites.add(player2)
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    Border(0, 0, width, 0)
    Border(0, height, width, height)
    Border(0, 0, 0, height)
    Border(width, 0, width, height)
    pygame.draw.rect(screen, pygame.Color('cyan'), (width // 2 - 5, 0, width // 2 + 5, height))
    center1 = Border(width // 2 - 5, 0, width // 2 - 5, height)
    center2 = Border(width // 2 + 5, 0, width // 2 + 5, height)
    all_sprites.add(center1)
    all_sprites.add(center2)
    clock = pygame.time.Clock()
    player_speed = 3
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_w]:
            newy = -player_speed
            player1.update(0, newy, 1)
        if keypress[pygame.K_s]:
            newy = player_speed
            player1.update(0, newy, 1)
        if keypress[pygame.K_d]:
            newx = player_speed
            player1.update(newx, 0, 1)
        if keypress[pygame.K_a]:
            newx = -player_speed
            player1.update(newx, 0, 1)
        if keypress[pygame.K_UP]:
            newy = -player_speed
            player2.update(0, newy, 2)
        if keypress[pygame.K_DOWN]:
            newy = player_speed
            player2.update(0, newy, 2)
        if keypress[pygame.K_RIGHT]:
            newx = player_speed
            player2.update(newx, 0, 2)
        if keypress[pygame.K_LEFT]:
            newx = -player_speed
            player2.update(newx, 0, 2)
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        clock.tick(60)
        pygame.draw.rect(screen, pygame.Color('cyan'), (width // 2 - 25, 0, 35, height))
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    vs()