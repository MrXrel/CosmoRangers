#  Created by X-Corporation


import os
import sys

import pygame

pygame.init()


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
        self.num = num
        self.health = 200
        self.shots = []
        self.damage = 20
        self.cooldown = 0
        self.image = pygame.transform.scale(self.image, [67, 55])
        if self.num == 1:
            self.laserim = pygame.transform.rotate(load_image('pixel_laser_yellow.png'), 90)
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect()
            self.rect.topleft = self.x, self.y
        elif self.num == 2:
            self.laserim = pygame.transform.rotate(load_image('pixel_laser_red.png'), 90)
            self.image = pygame.transform.rotate(self.image, 270)
            self.rect = self.image.get_rect()
            self.rect.topright = self.x, self.y

    def update(self, x, y):
        self.x = self.x + x
        self.y = self.y + y
        if self.num == 1:
            self.rect.topleft = self.x, self.y
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.y = self.y - y
                self.rect.topleft = self.x, self.y
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.x = self.x - x
                self.rect.topleft = self.x, self.y
        elif self.num == 2:
            self.rect.topright = self.x, self.y
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.y = self.y - y
                self.rect.topright = self.x, self.y
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.x = self.x - x
                self.rect.topright = self.x, self.y

    def shoot(self, speed):
        if self.cooldown == 0:
            if self.num == 1:
                shoot = Laser(self.x, self.y - self.image.get_height() + 50, self.laserim, speed)
            elif self.num == 2:
                shoot = Laser(self.x - 80, self.y - self.image.get_height() + 50, self.laserim, speed)
            self.shots.append(shoot)
            self.cooldown = 1

    def reset_reload(self):
        # if there is a reload add one every frame
        if self.cooldown != 0:
            self.cooldown += 1
        # if reload > 30, it half a second has passed
        if self.cooldown > 15:
            self.cooldown = 0

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


class Laser:
    def __init__(self, x, y, img, speed):
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.speed


def vs():
    size = width, height = 1000, 600
    font = pygame.font.SysFont('spacecur', 45)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("VS Mode Test")
    background = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background-black.png')),
                                        (width, height))
    global horizontal_borders
    global vertical_borders
    player1 = Player('spaceship_yellow.png', 25, height // 2 - 50, 1)
    player2 = Player('spaceship_red.png', width - 25, height // 2 - 50, 2)
    p1hp = font.render(f"Здоровье: {player1.health}", False, pygame.Color('white'))
    p2hp = font.render(f"Здоровье: {player2.health}", False, pygame.Color('white'))
    all_sprites.add(player1)
    all_sprites.add(player2)
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    Border(0, 0, width, 0)
    Border(0, height, width, height)
    Border(0, 0, 0, height)
    Border(width, 0, width, height)
    center1 = Border(width // 2 - 1, 0, width // 2 - 1, height)
    center2 = Border(width // 2 + 1, 0, width // 2 + 1, height)
    all_sprites.add(center1)
    all_sprites.add(center2)
    clock = pygame.time.Clock()
    player_speed = 3
    laser_speed = 4
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_w]:
            newy = -player_speed
            player1.update(0, newy)
        if keypress[pygame.K_s]:
            newy = player_speed
            player1.update(0, newy)
        if keypress[pygame.K_d]:
            newx = player_speed
            player1.update(newx, 0)
        if keypress[pygame.K_a]:
            newx = -player_speed
            player1.update(newx, 0)
        if keypress[pygame.K_SPACE]:
            player1.shoot(laser_speed)
        if keypress[pygame.K_UP]:
            newy = -player_speed
            player2.update(0, newy)
        if keypress[pygame.K_DOWN]:
            newy = player_speed
            player2.update(0, newy)
        if keypress[pygame.K_RIGHT]:
            newx = player_speed
            player2.update(newx, 0)
        if keypress[pygame.K_LEFT]:
            newx = -player_speed
            player2.update(newx, 0)
        if keypress[pygame.K_RCTRL]:
            player2.shoot(-laser_speed)
        screen.blit(background, (0, 0))
        screen.blit(p1hp, (25, 10))
        screen.blit(p2hp, (750, 10))
        all_sprites.draw(screen)
        for shot in player1.shots:
            shot.move()
        for shot in player2.shots:
            shot.move()
        player1.reset_reload()
        player2.reset_reload()
        for shot in player1.shots:
            shot.draw(screen)
        for shot in player2.shots:
            shot.draw(screen)
        clock.tick(60)
        pygame.draw.rect(screen, pygame.Color('white'), (width // 2 - 1, 0, 5, height))
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    vs()