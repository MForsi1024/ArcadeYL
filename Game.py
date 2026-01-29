import arcade
from arcade.gui import UIFlatButton, UIBoxLayout, UIAnchorLayout, UIManager, UISlider
from pyglet.graphics import Batch
from UI import UI
import random
import PIL
import PIL.Image
import PIL.ImageDraw
import math
import enum

class GlobalMain(UI):
    def __init__(self):
        super().__init__()
        self.manager.enable()
        self.create_textures()

        self.background = arcade.load_texture("resources/images/arcade_test_background.png")
        self.menu_text = arcade.Text("Подводная битва", self.window.width / 2, self.window.height * 0.75,
                                     arcade.color.WHITE, font_size=self.window.height * 0.037, anchor_x="center",
                                     batch=self.batch)
        self.background_color = arcade.color.BLUE_GRAY  # Фон для меню
        self.start_button = UIFlatButton(text="В бой!", width=self.window.width * 0.13, height=self.window.height * 0.14,
                                    style=self.button_style)

        self.start_button.on_click = lambda x: self.open_scene(SimpleBattlefield())
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

class FaceDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1


class Hero(arcade.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.window_width = width
        self.window_height = height

        # Основные характеристики
        self.scale = 1.0
        self.speed = 300
        self.health = 100

        # Загрузка текстур
        self.idle_texture = arcade.load_texture(
            ":resources:/images/animated_characters/male_person/malePerson_idle.png")
        self.texture = self.idle_texture

        self.walk_textures = []
        for i in range(0, 8):
            texture = arcade.load_texture(f":resources:/images/animated_characters/male_person/malePerson_walk{i}.png")
            self.walk_textures.append(texture)

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1  # секунд на кадр

        self.is_walking = False  # Никуда не идём
        self.face_direction = FaceDirection.RIGHT  # и смотрим вправо

        # Центрируем персонажа
        self.center_x = self.window_width // 2
        self.center_y = self.window_height // 2

    def update_animation(self, delta_time: float = 1 / 60):
        """ Обновление анимации """
        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.walk_textures):
                    self.current_texture = 0
                # Поворачиваем текстуру в зависимости от направления взгляда
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.walk_textures[self.current_texture]
                else:
                    self.texture = self.walk_textures[self.current_texture].flip_horizontally()

        else:
            # Если не идём, то просто показываем текстуру покоя
            # и поворачиваем её в зависимости от направления взгляда
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.idle_texture
            else:
                self.texture = self.idle_texture.flip_horizontally()

    def update(self, delta_time, keys_pressed):
        """ Перемещение персонажа """
        # В зависимости от нажатых клавиш определяем направление движения
        dx, dy = 0, 0
        if arcade.key.LEFT in keys_pressed or arcade.key.A in keys_pressed:
            dx -= self.speed * delta_time
        if arcade.key.RIGHT in keys_pressed or arcade.key.D in keys_pressed:
            dx += self.speed * delta_time
        if arcade.key.UP in keys_pressed or arcade.key.W in keys_pressed:
            dy += self.speed * delta_time
        if arcade.key.DOWN in keys_pressed or arcade.key.S in keys_pressed:
            dy -= self.speed * delta_time

        if dx != 0 and dy != 0:
            factor = 0.7071
            dx *= factor
            dy *= factor

        self.center_x += dx
        self.center_y += dy
        # Поворачиваем персонажа в зависимости от направления движения
        # Если никуда не идём, то не меняем направление взгляда
        if dx < 0:
            self.face_direction = FaceDirection.LEFT
        elif dx > 0:
            self.face_direction = FaceDirection.RIGHT

        # Ограничение в пределах экрана
        self.center_x = max(self.width / 2, min(self.window_width - self.width / 2, self.center_x))
        self.center_y = max(self.height / 2, min(self.window_height - self.height / 2, self.center_y))

        # Проверка на движение
        self.is_walking = dx or dy


class Enemy(arcade.Sprite):
    def __init__(self, x, y, width, height, speed=150, health=50):
        super().__init__()

        self.window_width = width
        self.window_height = height
        self.speed = speed
        self.health = health
        self.scale = 1.0

        # Загрузка текстур для врага
        self.idle_texture = arcade.load_texture(
            ":resources:/images/animated_characters/zombie/zombie_idle.png")
        self.texture = self.idle_texture

        self.walk_textures = []
        for i in range(0, 8):
            texture = arcade.load_texture(f":resources:/images/animated_characters/zombie/zombie_walk{i}.png")
            self.walk_textures.append(texture)

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.15
        self.is_walking = False
        self.face_direction = FaceDirection.RIGHT

        # Начальная позиция
        self.center_x = x
        self.center_y = y

        # Цель (герой)
        self.target = None

    def set_target(self, player):
        """Устанавливает цель для преследования"""
        self.target = player

    def update(self, delta_time):
        """Обновление позиции врага"""
        if not self.target:
            return

        # Рассчитываем направление к цели
        dx = self.target.center_x - self.center_x
        dy = self.target.center_y - self.center_y

        # Нормализуем вектор направления
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            dx = dx / distance * self.speed * delta_time
            dy = dy / distance * self.speed * delta_time

            # Обновляем позицию
            self.center_x += dx
            self.center_y += dy

            # Обновляем направление взгляда
            if dx < 0:
                self.face_direction = FaceDirection.LEFT
            elif dx > 0:
                self.face_direction = FaceDirection.RIGHT

            self.is_walking = True
        else:
            self.is_walking = False

        # Ограничение в пределах экрана
        self.center_x = max(self.width / 2, min(self.window_width - self.width / 2, self.center_x))
        self.center_y = max(self.height / 2, min(self.window_height - self.height / 2, self.center_y))

    def update_animation(self, delta_time: float = 1 / 60):
        """Обновление анимации врага"""
        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.walk_textures):
                    self.current_texture = 0
                # Поворачиваем текстуру в зависимости от направления взгляда
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.walk_textures[self.current_texture]
                else:
                    self.texture = self.walk_textures[self.current_texture].flip_horizontally()
        else:
            # Если не идём, показываем текстуру покоя
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.idle_texture
            else:
                self.texture = self.idle_texture.flip_horizontally()

    def take_damage(self, damage):
        """Получение урона"""
        self.health -= damage
        if self.health <= 0:
            self.remove_from_sprite_lists()
            return True  # Враг уничтожен
        return False

class Bullet(arcade.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y, width, height, speed=800, damage=10):
        super().__init__()
        self.texture = arcade.load_texture(":resources:/images/space_shooter/laserBlue01.png")
        self.center_x = start_x
        self.center_y = start_y
        self.speed = speed
        self.damage = damage
        self.window_width = width
        self.window_height = height

        # Рассчитываем направление
        x_diff = target_x - start_x
        y_diff = target_y - start_y
        angle = math.atan2(y_diff, x_diff)
        # И скорость
        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed
        # Если текстура ориентирована по умолчанию вправо, то поворачиваем пулю в сторону цели
        # Для другой ориентации нужно будет подправить угол
        self.angle = math.degrees(-angle)  # Поворачиваем пулю

    def update(self, delta_time):
        # Удаляем пулю, если она ушла за экран
        if (self.center_x < 0 or self.center_x > self.window_width or
                self.center_y < 0 or self.center_y >self.window_height):
            self.remove_from_sprite_lists()

        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time


class SimpleBattlefield(UI):
    def __init__(self):
        super().__init__()
        self.setup()
        arcade.set_background_color(arcade.color.ASH_GREY)

    def setup(self):
        # Создаём SpriteList для разных типов объектов
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()  # Добавляем список врагов
        self.all_sprites = arcade.SpriteList()  # Общий список для удобства

        # Создаём игрока
        self.player = Hero(self.window.width, self.window.height)
        self.player_list.append(self.player)
        self.all_sprites.append(self.player)

        # Создаём врагов
        self.create_enemies(5)  # Создаем 5 врагов

        # Создаём ящики (препятствия)
        wall_texture = arcade.load_texture(":resources:/images/tiles/boxCrate_double.png")
        for x in range(0, self.window.width, 128):
            wall = arcade.Sprite()
            wall.texture = wall_texture
            wall.center_x = x
            wall.center_y = 100
            self.wall_list.append(wall)
            self.all_sprites.append(wall)

        # Добавляем звуки
        self.shoot_sound = arcade.load_sound(":resources:/sounds/laser1.wav")
        self.enemy_hit_sound = arcade.load_sound(":resources:/sounds/hurt3.wav")
        self.enemy_death_sound = arcade.load_sound(":resources:/sounds/explosion2.wav")

        self.keys_pressed = set()

    def create_enemies(self, count):
        """Создаёт указанное количество врагов"""
        for i in range(count):
            # Случайная позиция по краям экрана
            side = random.randint(0, 3)
            if side == 0:  # Сверху
                x = random.randint(50, self.window.width - 50)
                y = self.window.height - 50
            elif side == 1:  # Справа
                x = self.window.width - 50
                y = random.randint(50, self.window.height - 50)
            elif side == 2:  # Снизу
                x = random.randint(50, self.window.width - 50)
                y = 50
            else:  # Слева
                x = 50
                y = random.randint(50, self.window.height - 50)

            enemy = Enemy(x, y, self.window.width, self.window.height)
            enemy.set_target(self.player)  # Устанавливаем цель - героя
            self.enemy_list.append(enemy)
            self.all_sprites.append(enemy)

    def on_draw(self):
        self.clear()
        # Рисуем все списки в правильном порядке
        self.wall_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()

    def on_update(self, delta_time):
        # Обновляем все списки
        self.player_list.update(delta_time, self.keys_pressed)
        self.enemy_list.update(delta_time)
        self.bullet_list.update()

        # Обновляем анимации
        self.player_list.update_animation()
        self.enemy_list.update_animation()

        # Проверяем столкновения пуль с врагами
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            for enemy in hit_list:
                bullet.remove_from_sprite_lists()
                if enemy.take_damage(bullet.damage):
                    arcade.play_sound(self.enemy_death_sound)
                else:
                    arcade.play_sound(self.enemy_hit_sound)
                break  # Пуля поражает только одного врага

        # Проверяем столкновения врагов с игроком
        for enemy in self.enemy_list:
            if arcade.check_for_collision(enemy, self.player):
                # Наносим урон игроку
                self.player.health -= 5
                enemy.center_x -= (enemy.center_x - self.player.center_x) * 0.1
                enemy.center_y -= (enemy.center_y - self.player.center_y) * 0.1

                if self.player.health <= 0:
                    # Игрок умер, можно добавить логику окончания игры
                    print("Игрок умер!")

        # Удаляем пули, вышедшие за экран
        for bullet in self.bullet_list:
            bullet.update(delta_time)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            bullet = Bullet(
                self.player.center_x,
                self.player.center_y,
                x,
                y,
                self.window.width,
                self.window.height,
            )
            self.bullet_list.append(bullet)
            # Проигрываем звук выстрела
            arcade.play_sound(self.shoot_sound)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

        # Можно добавить клавишу для создания новых врагов (для тестирования)
        if key == arcade.key.E:
            self.create_enemies(1)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)