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
        self.points = []
        COINS_COUNT = 10
        x = random.sample(range(50, self.window.width - 50, 50), COINS_COUNT)
        y = random.sample(range(int(self.window. height * 0.33), self.window.height - 50, 50),
                          COINS_COUNT)
        for i in range(COINS_COUNT):
            city = arcade.Sprite(":resources:images/items/coinGold.png", scale=1)
            city.center_x = x[i]
            city.center_y = y[i]
            self.cities.append(city)

        for i in range(3):
            self.cities[i].texture = arcade.load_texture(
                ":resources:/images/animated_characters/male_person/malePerson_idle.png")


    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мышью"""
        cities_hit_list = arcade.get_sprites_at_point((x, y), self.cities)  # В какие монеты тыкнул игрок.
        for city in cities_hit_list:
            for i in self.cities:
                i.texture = arcade.load_texture(":resources:images/items/coinGold.png")
            for i in range(3):
                self.cities[i].texture = arcade.load_texture(":resources:/images/animated_characters/male_person/malePerson_idle.png")
            self.new_texture = arcade.load_texture(":resources:images/animated_characters/female_person/femalePerson_idle.png")
            city.texture = self.new_texture




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

class Battlefield(UI):
    pass