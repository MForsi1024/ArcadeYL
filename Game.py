import arcade
from arcade.gui import UIFlatButton, UIBoxLayout, UIAnchorLayout, UIManager, UISlider
from pyglet.graphics import Batch
from UI import UI


class GlobalMain(UI):
    def __init__(self):
        super().__init__()
        self.manager.enable()
        self.background = arcade.load_texture("resources/images/arcade_test_background.png")
        self.menu_text = arcade.Text("Подводная битва", self.window.width / 2, self.window.height * 0.75,
                                     arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        self.background_color = arcade.color.BLUE_GRAY  # Фон для меню

        start_button = UIFlatButton(text="В бой!", width=250, height=150, color=arcade.color.BLUE,
                                    style=self.button_style)

        start_button.on_click = lambda x: print(0)
        self.manager.add(start_button)
        start_button.rect = start_button.rect.move(self.window.width - 275, 125)

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.rect.XYWH(self.width // 2, self.height // 2, self.width, self.height), pixelated=True
        )
        arcade.draw_lbwh_rectangle_filled(0, 0, self.width, 300, arcade.color.SAND)
        arcade.draw_lbwh_rectangle_outline(0, 0, self.width, 300, arcade.color.BLACK, 5)
        self.manager.draw()
