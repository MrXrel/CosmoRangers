import arcade
from menus import Title, Menu, WIDTH, HEIGHT


def start(load=0):
    window = arcade.Window(WIDTH, HEIGHT, "CosmoRangers")
    if load == 0:
        scene = Title()
        window.show_view(scene)
    else:
        scene = Menu()
        window.show_view(scene)
    arcade.run()


if __name__ == "__main__":
    start()