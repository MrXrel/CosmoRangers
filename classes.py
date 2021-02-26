from images import *
import pygame

all_sprites = pygame.sprite.Group()


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


class Ship(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, sheet, columns: int, rows: int, size: tuple, health=100):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.frames = []
        self.sheet = sheet
        transColor = self.sheet.get_at((0, 0))
        self.sheet.set_colorkey(transColor)
        self.cut_sheet(self.sheet, columns, rows)
        self.cur_frame = 0
        self.health = health
        self.img = None
        self.bullet_img = None
        self.size = size
        self.rect = self.rect.move(x, y)

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

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update_sprite(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.img = pygame.transform.scale(self.frames[self.cur_frame], self.size)
        self.mask = pygame.mask.from_surface(self.img)


class Player(Ship):
    def __init__(self, x, y, sheet, columns, rows, size, health=100):
        super().__init__(x, y, sheet, columns, rows, size)
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
    def __init__(self, x, y, bullet_speed, ship, columns, rows, size, health=100):
        sheet = ship[0]

        super().__init__(x, y, sheet, columns, rows, size)

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
                # TODO right shoot animation from center of the bot
                bullet = Bullet(self.x - (self.img.get_width() // 2) // 2, self.y - self.img.get_height() + 20, self.bullet_img, self.speed)
                enemy_bullets.append(bullet)
                self.reload = 1

    def reset_reload(self):
        # if there is a reload add one every frame
        if self.reload != 0:
            self.reload += 1
        # if reload > 30, it half a second has passed
        if self.reload > 70:
            self.reload = 0
