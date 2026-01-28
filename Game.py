import arcade
from arcade.gui import UIFlatButton, UIBoxLayout, UIAnchorLayout, UIManager, UISlider
from pyglet.graphics import Batch
from UI import UI
import random
import PIL
import PIL.Image
import PIL.ImageDraw
import math

class GlobalMain(UI):
    def __init__(self):
        super().__init__()
        self.manager.enable()
        self.create_textures()

        #начальная армия
        self.fighters = 3
        self.shooters = 3

        self.background = arcade.load_texture("resources/images/arcade_test_background.png")
        self.menu_text = arcade.Text("Подводная битва", self.window.width / 2, self.window.height * 0.75,
                                     arcade.color.WHITE, font_size=self.window.height * 0.037, anchor_x="center",
                                     batch=self.batch)
        self.background_color = arcade.color.BLUE_GRAY  # Фон для меню
        self.start_button = UIFlatButton(text="В бой!", width=self.window.width * 0.13, height=self.window.height * 0.14,
                                    style=self.button_style)

        self.start_button.on_click = lambda x: self.open_scene(SimpleBattlefield(self.fighters, self.shooters))
        self.manager.add(self.start_button)
        self.start_button.rect = self.start_button.rect.move(self.window.width * 0.85, 0.13 * self.window.height)

        self.player_cities = []
        self.cities = arcade.SpriteList()
        self.points = []
        COINS_COUNT = 10

        x = random.sample(range(25, self.window.width, 50), COINS_COUNT)
        y = random.sample(range(int(self.window.height * 0.33), self.window.height, 50),
                          COINS_COUNT)



        for i in range(COINS_COUNT):
            city = arcade.Sprite(self.red_circle_texture, scale=1)
            city.center_x = x[i]
            city.center_y = y[i]
            self.cities.append(city)

        for i in range(3):
            self.cities[i].texture = self.blue_circle_texture
            self.player_cities.append(i)

        self.start_button.disabled = True

    def create_textures(self):
        # синий круг
        image = PIL.Image.new('RGBA', (50, 50), (0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(image)
        draw.ellipse((5, 5, 45, 45), fill=(0, 0, 255, 255))
        self.blue_circle_texture = arcade.Texture(image)

        # красный круг
        image = PIL.Image.new('RGBA', (50, 50), (0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(image)
        draw.ellipse((5, 5, 45, 45), fill=(255, 36, 0, 255))
        self.red_circle_texture = arcade.Texture(image)

        # желтый круг
        image = PIL.Image.new('RGBA', (50, 50), (0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(image)
        draw.ellipse((5, 5, 45, 45), fill=(255, 255, 0, 255))
        self.yellow_circle_texture = arcade.Texture(image)

        # Текстура для бойцов (синий круг)
        image = PIL.Image.new('RGBA', (40, 40), (0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(image)
        draw.ellipse((5, 5, 35, 35), fill=(0, 0, 255, 255))  # Синий цвет
        self.fighter_texture = arcade.Texture(image)

        # Текстура для лучников (зеленый круг)
        image = PIL.Image.new('RGBA', (40, 40), (0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(image)
        draw.ellipse((5, 5, 35, 35), fill=(0, 255, 0, 255))  # Зеленый цвет
        self.shooter_texture = arcade.Texture(image)

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


class SimpleBattlefield(UI):
    def __init__(self, fighters, shooters):
        super().__init__()
        # Добавляем счетчики оставшихся юнитов
        self.fighters = fighters
        self.shooters = shooters

        # Добавляем список бойцов
        self.fighters_sprites = arcade.SpriteList()
        self.shooters_sprites = arcade.SpriteList()

        self.bullets = arcade.SpriteList()
        self.shoot_timer = 0

        # Кнопка возврата
        self.map = UIFlatButton(text="Вернуться на карту", width=150, height=50,
                                        style=self.button_style)
        self.map.on_click = lambda x: self.open_scene(GlobalMain())
        self.manager.add(self.map)
        self.map.rect = self.map.rect.move(
            self.width - 170, self.height - 70
        )
        self.map.disabled = True

        # Текст информации
        self.info_text = arcade.Text(
            f"Бойцов: {self.fighters} | Стрелков: {self.shooters}",
            20, self.height - 40,
            arcade.color.WHITE, 16
        )



    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.fighters > 0:
            # Создаем бойца (синий кружок)
            fighter = arcade.SpriteCircle(10, arcade.color.BLUE)
            fighter.center_x = x
            fighter.center_y = y
            self.fighters -= 1

            # добавляем солдат в список
            self.fighters_sprites.append(fighter)

            # Обновляем текст
            self.info_text.text = f"Бойцов: {self.fighters} | Стрелков: {self.shooters}"

        elif button == arcade.MOUSE_BUTTON_RIGHT and self.shooters > 0:
            # Создаем стрелка (зеленый кружок)
            shooter = arcade.SpriteCircle(10, arcade.color.GREEN)
            shooter.center_x = x
            shooter.center_y = y
            self.shooters -= 1

            #добавляем стрелков в список
            self.shooters_sprites.append(shooter)

            # Обновляем текст
            self.info_text.text = f"Бойцов: {self.fighters} | Стрелков: {self.shooters}"

    def on_update(self, delta_time):
        # Автострельба каждые 30 кадров
        self.shoot_timer += 1
        if self.shoot_timer >= 30:
            self.shoot_timer = 0
            self.auto_shoot()

        # Движение пуль вверх
        for bullet in self.bullets:
            bullet.center_y += 5
            if bullet.center_y > self.height:
                bullet.remove_from_sprite_lists()

        # Движение бойцов вверх
        for fighter in self.fighters_sprites:
            fighter.center_y += 1

        # Движение стрелков вверх (опционально)
        for shooter in self.shooters_sprites:
            shooter.center_y += 0.5  # Стрелки двигаются медленнее

        #если кончилась армия, покинуть бой
        if self.fighters_sprites == self.shooters_sprites == 0:
            self.map.disabled = False

    def auto_shoot(self):
        """Все стрелки стреляют вперед (вверх)"""
        for shooter in self.shooters_sprites:
            bullet = arcade.SpriteCircle(3, arcade.color.YELLOW)
            bullet.center_x = shooter.center_x
            bullet.center_y = shooter.center_y + 15  # Чуть выше стрелка
            self.bullets.append(bullet)

    def on_draw(self):
        self.clear()

        # Рисуем фон
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Рисуем всех юнитов
        self.fighters_sprites.draw()
        self.shooters_sprites.draw()
        self.bullets.draw()

        # Рисуем текст информации
        self.info_text.draw()

        # Рисуем интерфейс
        self.manager.draw()

