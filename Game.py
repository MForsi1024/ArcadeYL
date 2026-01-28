import arcade
from arcade.gui import UIFlatButton, UIBoxLayout, UIAnchorLayout, UIManager, UISlider
from pyglet.graphics import Batch
from UI import UI
import random
import PIL
import PIL.Image
import PIL.ImageDraw


class GlobalMain(UI):
    def __init__(self):
        super().__init__()
        self.manager.enable()
        self.background = arcade.load_texture("resources/images/arcade_test_background.png")
        self.menu_text = arcade.Text("Подводная битва", self.window.width / 2, self.window.height * 0.75,
                                     arcade.color.WHITE, font_size=self.window.height * 0.037, anchor_x="center",
                                     batch=self.batch)
        self.background_color = arcade.color.BLUE_GRAY  # Фон для меню
        self.start_button = UIFlatButton(text="В бой!", width=self.window.width * 0.13, height=self.window.height * 0.14,
                                    style=self.button_style)

        self.start_button.on_click = self.start_battle
        self.manager.add(self.start_button)
        self.start_button.rect = self.start_button.rect.move(self.window.width * 0.85, 0.13 * self.window.height)

        self.player_cities = []
        self.cities = arcade.SpriteList()
        self.points = []
        COINS_COUNT = 10

        x = random.sample(range(25, self.window.width, 50), COINS_COUNT)
        y = random.sample(range(int(self.window.height * 0.33), self.window.height, 50),
                          COINS_COUNT)

        #синий круг
        image = PIL.Image.new('RGBA', (50, 50), (0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(image)
        draw.ellipse((5, 5, 45, 45), fill=(0, 0, 255, 255))
        self.blue_circle_texture = arcade.Texture(image)

        #красный круг
        image = PIL.Image.new('RGBA', (50, 50), (0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(image)
        draw.ellipse((5, 5, 45, 45), fill=(255, 36, 0, 255))
        self.red_circle_texture = arcade.Texture(image)

        #желтый круг
        image = PIL.Image.new('RGBA', (50, 50), (0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(image)
        draw.ellipse((5, 5, 45, 45), fill=(255, 255, 0, 255))
        self.yellow_circle_texture = arcade.Texture(image)

        for i in range(COINS_COUNT):
            city = arcade.Sprite(self.red_circle_texture, scale=1)
            city.center_x = x[i]
            city.center_y = y[i]
            self.cities.append(city)

        for i in range(3):
            self.cities[i].texture = self.blue_circle_texture
            self.player_cities.append(i)

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мышью"""
        cities_hit_list = arcade.get_sprites_at_point((x, y), self.cities)  # В какие монеты тыкнул игрок.
        for city in cities_hit_list:
            for i in self.cities:
                i.texture = self.red_circle_texture
            for i in self.player_cities:
                self.cities[i].texture = self.blue_circle_texture
            self.new_texture = self.yellow_circle_texture
            if self.cities.index(city) in self.player_cities:
                self.start_button.disabled = True
            else:
                self.start_button.disabled = False
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

    def start_battle(self):
        pass

class Battlefield(UI):
    pass
