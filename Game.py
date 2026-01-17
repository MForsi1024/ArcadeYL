import arcade
from arcade.gui import UIFlatButton, UIBoxLayout, UIAnchorLayout, UIManager, UISlider
from pyglet.graphics import Batch
from UI import UI
import random


class GlobalMain(UI):
    def __init__(self):
        super().__init__()
        self.manager.enable()
        self.background = arcade.load_texture("resources/images/arcade_test_background.png")
        self.menu_text = arcade.Text("Подводная битва", self.window.width / 2, self.window.height * 0.75,
                                     arcade.color.WHITE, font_size=self.window.height * 0.037, anchor_x="center",
                                     batch=self.batch)
        self.background_color = arcade.color.BLUE_GRAY  # Фон для меню

        start_button = UIFlatButton(text="В бой!", width=self.window.width * 0.13, height=self.window.height * 0.14,
                                    color=arcade.color.BLUE,
                                    style=self.button_style)

        start_button.on_click = lambda x: print(self.points)
        self.manager.add(start_button)
        start_button.rect = start_button.rect.move(self.window.width * 0.85, 0.13 * self.window.height)

        self.cities = arcade.SpriteList()

        for _ in range(10):
            one_sprite = False
            self.points = []
            city = arcade.Sprite(":resources:images/items/coinGold.png", scale=0.5)
            x = random.randint(0, self.window.width)
            y = random.randint(int(self.window.height * 0.31), self.window.height)
            if (x, y) in self.points:
                while (x, y) in self.points:
                    x = random.randint(0, self.window.width)
                    y = random.randint(self.window.height * 0.31, self.window.height)

            city.center_x = x
            city.center_y = y

            for i in range(self.window.width):
                for j in range(self.window.height):
                    if (i - x) ** 2 + (j - y) ** 2 <= 5625:
                        self.points.append((i, j))

            self.cities.append(city)

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.rect.XYWH(self.width // 2, self.height // 2, self.width, self.height), pixelated=True
        )
        arcade.draw_lbwh_rectangle_filled(0, 0, self.width, self.window.height * 0.29, arcade.color.SAND)
        arcade.draw_lbwh_rectangle_outline(0, 0, self.width, self.window.height * 0.29, arcade.color.BLACK, 5)
        self.manager.draw()

        self.cities.draw()
