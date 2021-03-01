import arcade
from menus import Title, Menu, WIDTH, HEIGHT
import pygame


pygame.init()


def start(load=0):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('Assets/SpaceTitle.wav')
    pygame.mixer.music.set_volume(0.25)
    window = arcade.Window(WIDTH, HEIGHT, "CosmoRangers")
    if load == 0:
        scene = Title()
        window.show_view(scene)
    else:
        scene = Menu()
        window.show_view(scene)
    pygame.mixer.music.play(-1)
    arcade.run()


if __name__ == "__main__":
    start()
else:
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()