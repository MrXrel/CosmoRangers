import arcade
from arcade.gui import UIManager
from singleplayer import main
from VSMode import vs


WIDTH = 700
HEIGHT = 900


class Title(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("CosmoRangers", WIDTH / 2, HEIGHT / 2, arcade.color.CADET_BLUE,
                         font_size=42, anchor_x='center')
        arcade.draw_text("Press Enter", WIDTH / 2, HEIGHT / 2 - 50, arcade.color.AMAZON,
                         font_size=21, anchor_x='center')

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            scene = Menu()
            self.window.show_view(scene)


class Menu(arcade.View):
    def __init__(self):
        super(Menu, self).__init__()
        self.ui = UIManager(self.window)
        self.setup()

    def setup(self):
        self.ui.purge_ui_elements()
        self.ui.add_ui_element(arcade.gui.UILabel(
            'CosmoRangers', center_x=WIDTH / 2, center_y=800
        ))
        arcbtn = arcade.gui.UIFlatButton(
            "Arcade Mode", center_x=WIDTH // 2, center_y=600, width=400)
        arcbtn.set_handler("on_click", self.arcstart)
        self.ui.add_ui_element(arcbtn)
        vsbtn = arcade.gui.UIFlatButton(
            "VS Mode", center_x=WIDTH // 2, center_y=400, width=400)
        vsbtn.set_handler("on_click", self.vsstart)
        self.ui.add_ui_element(vsbtn)
        exitbtn = arcade.gui.UIFlatButton(
            "Exit", center_x=WIDTH // 2, center_y=200, width=400)
        exitbtn.set_handler("on_click", self.exit)
        self.ui.add_ui_element(exitbtn)

    def arcstart(self):
        arcade.close_window()
        try:
            scene = main()
            self.window.show_view(scene)
        except ValueError:
            pass

    def vsstart(self):
        arcade.close_window()
        try:
            scene = vs()
            self.window.show_view(scene)
        except ValueError:
            pass

    def exit(self):
        arcade.close_window()

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_draw(self):
        arcade.start_render()
