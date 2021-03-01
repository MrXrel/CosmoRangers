#  Created by X-Corporation


import os
import sys
import pygame

pygame.init()
pygame.font.init()


def load_image(name, colorkey=-1):
    fullname = os.path.join('Assets', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


all_sprites = pygame.sprite.Group()
font = pygame.font.Font('Assets/SpaceFont.ttf', 40)


class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y, num, col, row):
        super().__init__(all_sprites)
        self.frames = []
        self.srect = pygame.Rect(x, y, load_image(image).get_width() // col,
                                load_image(image).get_height() // row)
        self.sprite(load_image(image), col, row)
        self.spritecur = 0
        self.imname = image
        self.row = row
        self.col = col
        self.image = self.frames[self.spritecur]
        self.x = x
        self.y = y
        self.num = num
        self.health = 200
        self.shots = []
        self.damage = 40
        self.cooldown = 0
        self.revert = False
        self.count = 0
        self.trigger = False
        self.dtrigger = False
        self.image = pygame.transform.scale(self.image, [60, 86])
        if self.num == 1:
            self.rocketim = 'Projectiles/Rockets/BLUESMALLROCKET.png'
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect()
            self.rect.topleft = self.x, self.y
        elif self.num == 2:
            self.rocketim = 'Projectiles/Rockets/REDSMALLROCKET.png'
            self.image = pygame.transform.rotate(self.image, 270)
            self.rect = self.image.get_rect()
            self.rect.topright = self.x, self.y
        self.mask = pygame.mask.from_surface(self.image)

    def sprite(self, image, col, row):
        for j in range(row):
            for i in range(col):
                frame = (self.srect.w * i, self.srect.h * j)
                self.frames.append(image.subsurface(pygame.Rect(
                    frame, self.srect.size)))

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

    def framechange(self):
        if self.dtrigger and self.spritecur == 0 and self.count != 1:
            self.count += 1
        elif self.spritecur == 0 and self.count != 2 and self.trigger:
            self.revert = True
            self.count += 1
        elif self.trigger and self.spritecur == 0 and self.revert and self.count == 2:
            self.revert = False
            self.trigger = False
            self.count = 0
            self.frames = []
            self.srect = pygame.Rect(self.x, self.y, load_image(self.imname).get_width() // self.col,
                                        load_image(self.imname).get_height() // self.row)
            self.sprite(load_image(self.imname), self.col, self.row)
            self.image = self.frames[self.spritecur]
        elif self.dtrigger and self.count == 1 and self.spritecur == (len(self.frames) - 1):
            self.kill()
        self.image = self.frames[self.spritecur]
        if not self.dtrigger:
            self.image = pygame.transform.scale(self.image, [60, 86])
        else:
            self.image = pygame.transform.scale(self.image, [141, 150])
            if self.spritecur == 0:
                self.rect.center = self.rect.centerx - 20, self.y
        self.spritecur = (self.spritecur + 1) % len(self.frames)
        if self.num == 1:
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.num == 2:
            self.image = pygame.transform.rotate(self.image, 270)
        self.mask = pygame.mask.from_surface(self.image)

    def shoot(self, speed):
        if self.cooldown == 0:
            if self.num == 1:
                bang = Rocket(self.x + 20, self.y - self.image.get_height() + 82, self.rocketim, speed, 4, 1, 90)
            elif self.num == 2:
                bang = Rocket(self.x - 100, self.y - self.image.get_height() + 82, self.rocketim, speed, 4, 1, 270)
            self.shots.append(bang)
            self.cooldown = 1

    def reset_reload(self):
        if self.cooldown != 0:
            self.cooldown += 1
        if self.cooldown > 15:
            self.cooldown = 0

    def get_height(self):
        return self.y

    def get_width(self):
        return self.x

    def hit(self, image, col, row):
        self.spritecur = 0
        self.trigger = True
        self.frames = []
        self.srect = pygame.Rect(self.x, self.y, load_image(image).get_width() // col,
                                 load_image(image).get_height() // row)
        self.sprite(load_image(image), col, row)
        self.image = self.frames[self.spritecur]

    def death(self, image, col, row):
        self.spritecur = 0
        self.dtrigger = True
        self.frames = []
        self.srect = pygame.Rect(self.x, self.y, load_image(image).get_width() // col,
                                 load_image(image).get_height() // row)
        self.sprite(load_image(image), col, row)
        self.image = self.frames[self.spritecur]


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


class Rocket:
    def __init__(self, x, y, img, speed, col, row, degrees):
        self.x = x
        self.y = y
        self.frames = []
        self.srect = pygame.Rect(x, y, load_image(img).get_width() // col,
                                load_image(img).get_height() // row)
        self.sprite(load_image(img), col, row)
        self.spritecur = 0
        self.image = self.frames[self.spritecur]
        self.speed = speed
        self.rotate = degrees
        self.image = pygame.transform.scale(self.image, [17, 44])
        self.image = pygame.transform.rotate(self.image, self.rotate)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.speed

    def sprite(self, image, col, row):
        for j in range(row):
            for i in range(col):
                frame = (self.srect.w * i, self.srect.h * j)
                self.frames.append(image.subsurface(pygame.Rect(
                    frame, self.srect.size)))

    def framechange(self):
        self.image = self.frames[self.spritecur]
        self.spritecur = (self.spritecur + 1) % len(self.frames)
        self.image = pygame.transform.scale(self.image, [17, 44])
        self.image = pygame.transform.rotate(self.image, self.rotate)
        self.mask = pygame.mask.from_surface(self.image)

    def get_height(self):
        return self.y

    def get_width(self):
        return self.x


def collide(shot, ship, num) -> bool:
    if num == 1:
        return shot.mask.overlap(ship.mask, (ship.x - shot.x - 70, ship.y - shot.y))
    elif num == 2:
        return shot.mask.overlap(ship.mask, (ship.x - shot.x, ship.y - shot.y))


def vs():
    pygame.init()
    all_sprites = pygame.sprite.Group()
    font = pygame.font.Font('Assets/SpaceFont.ttf', 40)

    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("CosmoRangers VS Mode")
    background = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background-black.png')),
                                        (width, height))
    global horizontal_borders
    global vertical_borders
    player1 = Player('Ships/Flying/BLUEVOYAGERSHEET.png', 25, height // 2 - 50, 1, 4, 1)
    player2 = Player('Ships/Flying/REDVOYAGERSHEET.png', width - 25, height // 2 - 50, 2, 4, 1)
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
    rocket_speed = 5
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keypress = pygame.key.get_pressed()
        if not player1.dtrigger:
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
                player1.shoot(rocket_speed)
        if not player2.dtrigger:
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
                player2.shoot(-rocket_speed)
        if player1.dtrigger or player2.dtrigger:
            if keypress[pygame.K_ESCAPE]:
                running = False
            if keypress[pygame.K_r]:
                vs()
        screen.blit(background, (0, 0))
        p1hp = font.render(f"Здоровье: {player1.health}", False, pygame.Color('white'))
        p2hp = font.render(f"Здоровье: {player2.health}", False, pygame.Color('white'))
        for shot in player1.shots:
            shot.move()
            shot.framechange()
            if collide(shot, player2, 1):
                player1.shots.remove(shot)
                player2.health -= player1.damage
                if player2.health > 0:
                    player2.hit('Ships/Damage/REDVOYAGERDAMAGE.png', 4, 1)
                else:
                    player2.death('Ships/Death/REDVOYAGERDEATH.png', 4, 3)
            if shot.x - shot.image.get_width() >= width:
                player1.shots.remove(shot)
        for shot in player2.shots:
            shot.move()
            shot.framechange()
            if collide(shot, player1, 2):
                player2.shots.remove(shot)
                player1.health -= player2.damage
                if player1.health > 0:
                    player1.hit('Ships/Damage/BLUEVOYAGERDAMAGE.png', 4, 1)
                else:
                    player1.death('Ships/Death/BLUEVOYAGERDEATH.png', 4, 3)
            if shot.x - shot.image.get_width() == 0:
                player2.shots.remove(shot)
        player1.reset_reload()
        player2.reset_reload()
        for shot in player1.shots:
            shot.draw(screen)
        for shot in player2.shots:
            shot.draw(screen)
        player1.framechange()
        player2.framechange()
        all_sprites.draw(screen)
        screen.blit(p1hp, (20, 10))
        screen.blit(p2hp, (550, 10))
        pygame.draw.rect(screen, pygame.Color('dark blue'), (width // 2 - 1, 0, 5, height))
        if player2.dtrigger:
            victory = font.render('Первый игрок победил!', False, pygame.Color('white'))
            cont = font.render('Нажмите "ESC", чтобы выйти', False,
                               pygame.Color('white'))
            cont2 = font.render('Нажмите "R", чтобы перезапустить', False,
                               pygame.Color('white'))
            screen.blit(victory, (150, height / 2 - 200))
            screen.blit(cont, (150, height / 2 - 100))
            screen.blit(cont2, (150, height / 2))
        elif player1.dtrigger:
            victory = font.render('Второй игрок победил!', False, pygame.Color('white'))
            cont = font.render('Нажмите "ESC", чтобы выйти', False,
                               pygame.Color('white'))
            cont2 = font.render('Нажмите "R", чтобы перезапустить', False,
                                pygame.Color('white'))
            screen.blit(victory, (150, height / 2 - 200))
            screen.blit(cont, (150, height / 2 - 100))
            screen.blit(cont2, (150, height / 2))
        clock.tick(30)
        pygame.display.flip()
    pygame.quit()
    from CosmoRangers import start
    start(1)


if __name__ == '__main__':
    vs()