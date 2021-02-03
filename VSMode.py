#  Created by X-Corporation


import os
import sys

import pygame

pygame.init()
size = width, height = 900, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("VS Mode Test")


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        if num == 1:
            self.rect.topleft = self.x, self.y
        elif num == 2:
            self.rect.topright = self.x, self.y

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


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


player1 = Player('ship.png', 0, height / 2, 1)
player2 = Player('ship.png', width, height // 2, 2)
all_sprites.add(player1)
all_sprites.add(player2)
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
Border(0, 0, width, 0)
Border(0, height, width, height)
Border(0, 0, 0, height)
Border(width, 0, width, height)
Border(width // 2, 0, width // 2, height)
running = True
keypress = pygame.key.get_pressed()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keypress = pygame.key.get_pressed()
    if keypress[pygame.K_w]:
        newy = -1
        player1.update(0, newy, 1)
    if keypress[pygame.K_s]:
        y1 = 1
        player1.update(0, newy, 1)
    if keypress[pygame.K_d]:
        newx = 1
        player1.update(newx, 0, 1)
    if keypress[pygame.K_a]:
        newx = -1
        player1.update(newx, 0, 1)
    if keypress[pygame.K_UP]:
        newy = -1
        player2.update(0, newy, 2)
    if keypress[pygame.K_DOWN]:
        newy = 1
        player2.update(0, newy, 2)
    if keypress[pygame.K_RIGHT]:
        newx = 1
        player2.update(newx, 0, 2)
    if keypress[pygame.K_LEFT]:
        newx = -1
        player2.update(newx, 0, 2)
    screen.fill(pygame.Color("white"))
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()

pygame.quit()