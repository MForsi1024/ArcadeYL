from arcade import Camera2D
from UI import *
import random
import PIL
import PIL.Image
import PIL.ImageDraw
import math
import enum
import time
import Particles

# Глобальная переменная для общего времени прохождения
TOTAL_GAME_TIME = 0
# Словарь для хранения времени на каждом уровне
LEVEL_TIMES = {}
# Глобальное состояние карты
GLOBAL_MAP_STATE = {
    'player_cities': [0, 1, 2],  # Начальные города игрока
    'cities_data': [],
    'selected_city_index': None
}


class GlobalMain(UI):
    def __init__(self, restore_state=False):
        super().__init__()


        global GLOBAL_MAP_STATE
        self.player_cities = GLOBAL_MAP_STATE['player_cities'].copy()
        self.selected_city_index = GLOBAL_MAP_STATE['selected_city_index']
        self.cities_data = GLOBAL_MAP_STATE['cities_data'].copy()

        self.manager.enable()
        self.create_textures()

        self.background = arcade.load_texture("resources/images/background.png")
        self.menu_text = arcade.Text("Подводная битва", self.window.width / 2, self.window.height * 0.75,
                                     arcade.color.WHITE, font_size=self.window.height * 0.037, anchor_x="center",
                                     batch=self.batch)
        self.background_color = arcade.color.BLUE_GRAY
        self.start_button = UIFlatButton(text="В бой!", width=self.window.width * 0.13,
                                         height=self.window.height * 0.14,
                                         style=self.button_style)

        self.start_button.on_click = lambda x: self.start_battle()
        self.manager.add(self.start_button)
        self.start_button.rect = self.start_button.rect.move(self.window.width * 0.85, 0.13 * self.window.height)

        self.cities = arcade.SpriteList()
        COINS_COUNT = 10

        if self.cities_data:
            for city_data in self.cities_data:
                city = arcade.Sprite(self.red_circle_texture, scale=1)
                city.center_x = city_data['x']
                city.center_y = city_data['y']
                city.index = city_data['index']
                city.order = city_data.get('order', city_data['index'])
                self.cities.append(city)
        else:
            # Иначе создаем новые города
            x = random.sample(range(25, self.window.width, 50), COINS_COUNT)
            y = random.sample(range(int(self.window.height * 0.33), self.window.height, 50), COINS_COUNT)

            for i in range(COINS_COUNT):
                city = arcade.Sprite(self.red_circle_texture, scale=1)
                city.center_x = x[i]
                city.center_y = y[i]
                city.index = i
                city.order = i
                self.cities.append(city)
                self.cities_data.append({'x': x[i], 'y': y[i], 'index': i, 'order': i})

            GLOBAL_MAP_STATE['cities_data'] = self.cities_data.copy()

        # Восстанавливаем состояние захваченных городов
        for i in self.player_cities:
            if i < len(self.cities):
                self.cities[i].texture = self.blue_circle_texture

        if self.selected_city_index is not None and self.selected_city_index < len(self.cities):
            if self.selected_city_index not in self.player_cities:
                self.cities[self.selected_city_index].texture = self.yellow_circle_texture
                self.start_button.disabled = False
            else:
                self.start_button.disabled = True
                self.selected_city_index = None
        else:
            self.start_button.disabled = True

    def start_battle(self):
        """Запускает битву с передачей индекса города"""
        if self.selected_city_index is not None and self.selected_city_index not in self.player_cities:

            battlefield = SimpleBattlefield()
            battlefield.selected_city_index = self.selected_city_index
            for city in self.cities:
                if city.index == self.selected_city_index:
                    battlefield.level_number = city.order + 1
                    break
            self.open_scene(battlefield)

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

        # серый круг (недоступные города)
        image = PIL.Image.new('RGBA', (50, 50), (0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(image)
        draw.ellipse((5, 5, 45, 45), fill=(128, 128, 128, 255))
        self.gray_circle_texture = arcade.Texture(image)

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мышью"""
        cities_hit_list = arcade.get_sprites_at_point((x, y), self.cities)
        for city in cities_hit_list:
            city_index = city.index
            city_order = city.order

            # Проверяем, доступен ли этот город
            max_captured_order = max(
                [c.order for c in self.cities if c.index in self.player_cities]) if self.player_cities else -1

            # Город доступен только если предыдущий по порядку захвачен
            if city_order > max_captured_order + 1:
                # Этот город еще недоступен
                self.start_button.disabled = True
                self.selected_city_index = None
                return

            # Сбрасываем все города на красные/серые
            for i in self.cities:
                i_order = i.order
                # Недоступные города делаем серыми
                if i_order > max_captured_order + 1:
                    i.texture = self.gray_circle_texture
                elif i.index not in self.player_cities:
                    i.texture = self.red_circle_texture

            # Восстанавливаем синие (захваченные) города
            for i in self.player_cities:
                if i < len(self.cities):
                    self.cities[i].texture = self.blue_circle_texture

            if city_index in self.player_cities:
                self.start_button.disabled = True
                self.selected_city_index = None
            else:
                self.start_button.disabled = False
                self.selected_city_index = city_index
                city.texture = self.yellow_circle_texture

    def capture_city(self, city_index):
        """Захватываем город после победы на уровне"""
        if city_index is not None and city_index not in self.player_cities:
            self.player_cities.append(city_index)

            # Обновляем глобальное состояние
            global GLOBAL_MAP_STATE
            GLOBAL_MAP_STATE['player_cities'] = self.player_cities.copy()

            if city_index < len(self.cities):
                self.cities[city_index].texture = self.blue_circle_texture
            self.selected_city_index = None
            self.start_button.disabled = True

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.rect.XYWH(self.width // 2, self.height // 2, self.width, self.height), pixelated=True
        )
        arcade.draw_lbwh_rectangle_filled(0, 0, self.width, self.window.height * 0.29, arcade.color.SAND)
        arcade.draw_lbwh_rectangle_outline(0, 0, self.width, self.window.height * 0.29, arcade.color.BLACK, 5)

        # Рисуем линии между городами по порядку
        sorted_cities = sorted(self.cities, key=lambda c: c.order)
        for i in range(len(sorted_cities) - 1):
            city1 = sorted_cities[i]
            city2 = sorted_cities[i + 1]

            # Определяем цвет линии в зависимости от доступности
            max_captured_order = max(
                [c.order for c in self.cities if c.index in self.player_cities]) if self.player_cities else -1

            if i <= max_captured_order:
                line_color = arcade.color.BLUE  # Пройденный путь
            elif i == max_captured_order:
                line_color = arcade.color.YELLOW  # Текущий доступный
            else:
                line_color = arcade.color.GRAY  # Еще недоступный

            arcade.draw_line(city1.center_x, city1.center_y,
                             city2.center_x, city2.center_y,
                             line_color, 3)

        # Отображаем номера городов
        for city in self.cities:
            arcade.draw_text(
                str(city.order + 1),  # Показываем с 1, а не с 0
                city.center_x,
                city.center_y + 35,
                arcade.color.WHITE,
                16,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

        # Отображаем статистику
        stats_text = f"Под контролем: {len(self.player_cities)} из {len(self.cities)} городов"
        arcade.draw_text(
            stats_text,
            self.window.width // 2,
            self.window.height * 0.25,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            anchor_y="center"
        )

        # Отображаем общее время игры
        global TOTAL_GAME_TIME
        if TOTAL_GAME_TIME > 0:
            time_text = f"Общее время: {TOTAL_GAME_TIME:.1f} сек"
            arcade.draw_text(
                time_text,
                self.window.width // 2,
                self.window.height * 0.18,
                arcade.color.GOLD,
                18,
                anchor_x="center",
                anchor_y="center"
            )

        self.manager.draw()
        self.cities.draw()

    def save_state(self):
        """Сохраняет текущее состояние карты"""
        global GLOBAL_MAP_STATE
        GLOBAL_MAP_STATE['player_cities'] = self.player_cities.copy()
        GLOBAL_MAP_STATE['selected_city_index'] = self.selected_city_index
        GLOBAL_MAP_STATE['cities_data'] = self.cities_data.copy()


class SettingsMenu(UI):
    """Меню настроек"""

    def __init__(self):
        super().__init__()
        self.manager.enable()

        # Фон
        self.background = arcade.load_texture("resources/images/background.png")

        # Заголовок
        self.title = arcade.Text(
            "НАСТРОЙКИ",
            self.window.width // 2,
            self.window.height * 0.85,
            arcade.color.WHITE,
            60,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        # Кнопки
        self.back_button = UIFlatButton(
            text="Назад",
            width=self.window.width * 0.2,
            height=self.window.height * 0.08,
            style=self.button_style
        )
        self.back_button.on_click = lambda x: self.return_to_main_menu()

        # Слайдер для громкости
        self.volume_label = arcade.Text(
            "Громкость звука:",
            self.window.width // 2,
            self.window.height * 0.6,
            arcade.color.WHITE,
            24,
            anchor_x="center",
            anchor_y="center"
        )

        self.volume_slider = UISlider(value=50, width=300, height=20)

        # Добавляем элементы
        self.manager.add(self.back_button)
        self.manager.add(self.volume_slider)

        # Позиционируем элементы
        self.back_button.rect = self.back_button.rect.move(
            self.window.width // 2 - self.back_button.width // 2,
            self.window.height * 0.2
        )

        self.volume_slider.rect = self.volume_slider.rect.move(
            self.window.width // 2 - self.volume_slider.width // 2,
            self.window.height * 0.55
        )

    def on_draw(self):
        self.clear()

        # Фон
        arcade.draw_texture_rect(
            self.background,
            arcade.rect.XYWH(self.width // 2, self.height // 2, self.width, self.height),
            pixelated=True
        )

        # Затемняющий фон для меню
        arcade.draw_lbwh_rectangle_filled(
            self.window.width // 2 - 250,
            self.window.height // 2 - 200,
            500,
            400,
            (0, 0, 0, 200)  # Полупрозрачный черный
        )

        # Текст
        self.title.draw()
        self.volume_label.draw()

        # UI элементы
        self.manager.draw()

    def return_to_main_menu(self):
        """Возврат в главное меню"""
        main_view = GlobalMain(restore_state=True)
        self.open_scene(main_view)


class FaceDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1


class Hero(arcade.Sprite):

    def __init__(self, width, height):
        super().__init__()

        self.window_width = width
        self.window_height = height
        self.scale = 0.5
        self.speed = 300
        self.health = 1
        self.alive = True

        self.idle_texture = arcade.load_texture(
            "resources/images/persons/green/green1.png")
        self.texture = self.idle_texture

        self.walk_textures = []
        for i in range(2, 5):
            texture = arcade.load_texture(f"resources/images/persons/green/green{i}.png")
            self.walk_textures.append(texture)

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1
        self.is_walking = False
        self.face_direction = FaceDirection.RIGHT

        self.center_x = self.window_width // 2
        self.center_y = self.window_height // 2

    def update_animation(self, delta_time):
        if not self.alive:
            return

        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.walk_textures):
                    self.current_texture = 0
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.walk_textures[self.current_texture]
                else:
                    self.texture = self.walk_textures[self.current_texture].flip_horizontally()
        else:
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.idle_texture
            else:
                self.texture = self.idle_texture.flip_horizontally()

    def update(self, delta_time, keys_pressed):
        if not self.alive:
            return

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

        if dx < 0:
            self.face_direction = FaceDirection.LEFT
        elif dx > 0:
            self.face_direction = FaceDirection.RIGHT

        self.center_x = max(self.width / 2, min(self.window_width - self.width / 2, self.center_x))
        self.center_y = max(self.height / 2, min(self.window_height - self.height / 2, self.center_y))

        self.is_walking = dx or dy

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            self.remove_from_sprite_lists()
            return True
        return False


class Enemy(arcade.Sprite):
    def __init__(self, x, y, width, height, ui,speed=100, health=25):
        super().__init__()
        self.window_width = width
        self.window_height = height
        self.speed = speed
        self.health = health
        self.scale = 0.5
        self.damage = 100
        self.ui = ui
        self.idle_texture = arcade.load_texture(
            "resources/images/persons/red/red1.png")
        self.texture = self.idle_texture

        self.walk_textures = []
        for i in range(2, 5):
            texture = arcade.load_texture(f"resources/images/persons/red/red{i}.png")
            self.walk_textures.append(texture)

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.15
        self.is_walking = False
        self.face_direction = FaceDirection.RIGHT

        self.center_x = x
        self.center_y = y
        self.target = None

    def set_target(self, player):
        self.target = player

    def update(self, delta_time):
        if not self.target:
            return

        dx = self.target.center_x - self.center_x
        dy = self.target.center_y - self.center_y

        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 10:
            dx = dx / distance * self.speed * delta_time
            dy = dy / distance * self.speed * delta_time

            self.center_x += dx
            self.center_y += dy

            if dx < 0:
                self.face_direction = FaceDirection.LEFT
            elif dx > 0:
                self.face_direction = FaceDirection.RIGHT

            self.is_walking = True
        else:
            self.is_walking = False
        self.center_x = max(self.width / 2, min(self.window_width - self.width / 2, self.center_x))
        self.center_y = max(self.height / 2, min(self.window_height - self.height / 2, self.center_y))

    def update_animation(self, delta_time):
        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.walk_textures):
                    self.current_texture = 0
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.walk_textures[self.current_texture]
                else:
                    self.texture = self.walk_textures[self.current_texture].flip_horizontally()
        else:
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.idle_texture
            else:
                self.texture = self.idle_texture.flip_horizontally()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.ui.emitters.append(Particles.make_smoke_puff(self.center_x, self.center_y))
            self.remove_from_sprite_lists()
            return True
        return False


class EnemyBullet(arcade.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y, width, height, speed=300, damage=100):
        super().__init__()
        self.texture = arcade.load_texture("resources/images/bullet.png")
        self.scale = 0.5
        self.center_x = start_x
        self.center_y = start_y
        self.speed = speed
        self.damage = damage

        self.window_width = width
        self.window_height = height

        x_diff = target_x - start_x
        y_diff = target_y - start_y
        angle = math.atan2(y_diff, x_diff)
        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed
        self.angle = math.degrees(-angle)

    def update(self, delta_time):
        if (self.center_x < 0 or self.center_x > self.window_width or
                self.center_y < 0 or self.center_y > self.window_height):
            self.remove_from_sprite_lists()
            return

        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time


class Bullet(arcade.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y, width, height, speed=800, damage=10):
        super().__init__()
        self.texture = arcade.load_texture("resources/images/bullet.png")
        self.scale = 0.5
        self.center_x = start_x
        self.center_y = start_y
        self.speed = speed
        self.damage = damage
        self.window_width = width
        self.window_height = height

        x_diff = target_x - start_x
        y_diff = target_y - start_y
        angle = math.atan2(y_diff, x_diff)
        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed
        self.angle = math.degrees(-angle)

    def update(self, delta_time):
        if (self.center_x < 0 or self.center_x > self.window_width or
                self.center_y < 0 or self.center_y > self.window_height):
            self.remove_from_sprite_lists()

        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time


class SimpleBattlefield(UI):
    def __init__(self):
        super().__init__()
        self.level_number = 1
        self.selected_city_index = None
        self.level_start_time = time.time()
        self.level_time = 0
        self.setup()
        arcade.set_background_color(arcade.color.ASH_GREY)
        self.game_over = False
        self.level_complete = False
        self.emitters = []
        self.world_camera = Camera2D()
        self.gui_camera = Camera2D()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()

        self.game_over = False
        self.level_complete = False
        self.level_start_time = time.time()  # Сбрасываем таймер уровня

        self.player = Hero(self.window.width, self.window.height)
        self.player_list.append(self.player)

        # Количество врагов зависит от номера уровня
        enemy_count = 5 + min(self.level_number * 2, 15)  # Увеличиваем сложность с каждым уровнем
        self.create_enemies(enemy_count)

        wall_texture = arcade.load_texture("resources/images/box.png")
        for x in range(0, self.window.width, 128):
            wall = arcade.Sprite()
            wall.texture = wall_texture
            wall.scale = 0.5
            wall.center_x = x
            wall.center_y = 100
            self.wall_list.append(wall)

        self.shoot_sound = arcade.load_sound(":resources:/sounds/laser1.wav")
        self.enemy_hit_sound = arcade.load_sound(":resources:/sounds/hurt3.wav")
        self.enemy_death_sound = arcade.load_sound(":resources:/sounds/explosion2.wav")
        self.player_death_sound = arcade.load_sound(":resources:/sounds/gameover3.wav")
        self.level_complete_sound = arcade.load_sound(":resources:/sounds/upgrade1.wav")

        self.keys_pressed = set()
        self.enemy_attack_timer = 0
        self.enemy_attack_cooldown = 1.5

    def create_enemies(self, count):
        for i in range(count):
            side = random.randint(0, 3)
            if side == 0:
                x = random.randint(50, self.window.width - 50)
                y = self.window.height - 50
            elif side == 1:
                x = self.window.width - 50
                y = random.randint(50, self.window.height - 50)
            elif side == 2:
                x = random.randint(50, self.window.width - 50)
                y = 50
            else:
                x = 50
                y = random.randint(50, self.window.height - 50)

            enemy = Enemy(x, y, self.window.width, self.window.height, self)
            enemy.set_target(self.player)
            self.enemy_list.append(enemy)

    def on_draw(self):
        self.clear()

        if self.game_over:
            arcade.draw_lbwh_rectangle_filled(
                0, 0,
                self.window.width,
                self.window.height,
                arcade.color.BLACK
            )

            game_over_text = arcade.Text(
                "ИГРА ОКОНЧЕНА",
                self.window.width // 2,
                self.window.height // 2,
                arcade.color.RED,
                60,
                anchor_x="center",
                anchor_y="center"
            )
            restart_text = arcade.Text(
                "Нажмите R для перезапуска",
                self.window.width // 2,
                self.window.height // 2 - 80,
                arcade.color.WHITE,
                30,
                anchor_x="center",
                anchor_y="center"
            )

            game_over_text.draw()
            restart_text.draw()
            return

        if self.level_complete:
            arcade.draw_lbwh_rectangle_filled(
                0, 0,
                self.window.width,
                self.window.height,
                arcade.color.DARK_GREEN
            )

            complete_text = arcade.Text(
                "УРОВЕНЬ ПРОЙДЕН!",
                self.window.width // 2,
                self.window.height // 2 + 60,
                arcade.color.GOLD,
                60,
                anchor_x="center",
                anchor_y="center"
            )
            return_text = arcade.Text(
                "Нажмите SPACE для продолжения",
                self.window.width // 2,
                self.window.height // 2 - 20,
                arcade.color.WHITE,
                30,
                anchor_x="center",
                anchor_y="center"
            )

            # Показываем время прохождения уровня
            time_text = arcade.Text(
                f"Время уровня: {self.level_time:.1f} сек",
                self.window.width // 2,
                self.window.height // 2 - 70,
                arcade.color.YELLOW,
                24,
                anchor_x="center",
                anchor_y="center"
            )

            complete_text.draw()
            return_text.draw()
            time_text.draw()
            return

        self.wall_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.enemy_bullet_list.draw()

        # Отображаем время уровня
        current_time = time.time() - self.level_start_time
        time_text = f"Уровень {self.level_number}: {current_time:.1f} сек"
        arcade.draw_text(
            time_text,
            10,
            self.window.height - 30,
            arcade.color.WHITE,
            20
        )
        self.world_camera.use()
        self.gui_camera.use()
        for e in self.emitters:
            e.draw()

    def on_update(self, delta_time):
        if self.game_over or self.level_complete:
            return

        # Обновляем время уровня
        self.level_time = time.time() - self.level_start_time

        self.player_list.update(delta_time, self.keys_pressed)
        self.enemy_list.update(delta_time)
        self.bullet_list.update()
        self.enemy_bullet_list.update()

        self.player_list.update_animation()
        self.enemy_list.update_animation()
        target = (self.player.center_x, self.player.center_y)
        cx, cy = self.world_camera.position
        smooth = (cx + (target[0] - cx) * 0.12,
                  cy + (target[1] - cy) * 0.12)

        half_w = self.world_camera.viewport_width / 2
        half_h = self.world_camera.viewport_height / 2
        world_w = 2000
        world_h = 900
        cam_x = max(half_w, min(world_w - half_w, smooth[0]))
        cam_y = max(half_h, min(world_h - half_h, smooth[1]))

        self.world_camera.position = (cam_x, cam_y)
        self.gui_camera.position = (self.width / 2, self.height / 2)
        if len(self.enemy_list) == 0:
            self.level_complete = True
            arcade.play_sound(self.level_complete_sound)
            return

        self.enemy_attack_timer += delta_time
        if self.enemy_attack_timer >= self.enemy_attack_cooldown:
            self.enemy_attack_timer = 0
            for enemy in self.enemy_list:
                if random.random() < 0.3:
                    bullet = EnemyBullet(
                        enemy.center_x,
                        enemy.center_y,
                        self.player.center_x,
                        self.player.center_y,
                        self.window.width,
                        self.window.height
                    )
                    self.enemy_bullet_list.append(bullet)

        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            for enemy in hit_list:
                bullet.remove_from_sprite_lists()
                if enemy.take_damage(bullet.damage):
                    arcade.play_sound(self.enemy_death_sound)
                else:
                    arcade.play_sound(self.enemy_hit_sound)
                break

        for bullet in self.enemy_bullet_list:
            if arcade.check_for_collision(bullet, self.player):
                bullet.remove_from_sprite_lists()
                if self.player.take_damage(bullet.damage):
                    arcade.play_sound(self.player_death_sound)
                    self.game_over = True
                    return

        for enemy in self.enemy_list:
            if arcade.check_for_collision(enemy, self.player):
                if self.player.take_damage(enemy.damage):
                    arcade.play_sound(self.player_death_sound)
                    self.game_over = True
                    return

        for bullet in list(self.bullet_list):
            bullet.update(delta_time)
        for bullet in list(self.enemy_bullet_list):
            bullet.update(delta_time)

        emitters_copy = self.emitters.copy()  # Защищаемся от мутаций списка
        for e in emitters_copy:
            e.update(delta_time)
    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_over or self.level_complete:
            return

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
            arcade.play_sound(self.shoot_sound)

    def on_key_press(self, key, modifiers):
        if self.game_over:
            if key == arcade.key.R:
                self.setup()
            return

        if self.level_complete:
            if key == arcade.key.SPACE:
                # Сохраняем время уровня
                global LEVEL_TIMES, TOTAL_GAME_TIME
                LEVEL_TIMES[self.level_number] = self.level_time
                TOTAL_GAME_TIME += self.level_time

                # Создаем новую карту с сохраненным состоянием
                main_view = GlobalMain(restore_state=True)

                # Захватываем город
                if self.selected_city_index is not None:
                    main_view.capture_city(self.selected_city_index)
                    # Сохраняем состояние после захвата
                    main_view.save_state()

                # Проверяем, все ли города захвачены
                if len(main_view.player_cities) >= 10:
                    victory_screen = VictoryScreen(
                        level_times=LEVEL_TIMES,
                        total_time=TOTAL_GAME_TIME
                    )
                    self.open_scene(victory_screen)
                else:
                    self.open_scene(main_view)
                return

        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)


class VictoryScreen(UI):
    def __init__(self, level_times=None, total_time=0):
        super().__init__()
        self.level_times = level_times if level_times else {}
        self.total_time = total_time
        self.manager.enable()

        self.title_text = arcade.Text(
            "ПОБЕДА!",
            self.window.width // 2,
            self.window.height * 0.85,
            arcade.color.GOLD,
            80,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        self.subtitle_text = arcade.Text(
            "Все города захвачены!",
            self.window.width // 2,
            self.window.height * 0.77,
            arcade.color.WHITE,
            36,
            anchor_x="center",
            anchor_y="center"
        )

        self.total_time_text = arcade.Text(
            f"Общее время прохождения: {self.total_time:.1f} секунд",
            self.window.width // 2,
            self.window.height * 0.65,
            arcade.color.YELLOW,
            32,
            anchor_x="center",
            anchor_y="center"
        )

        self.table_title = arcade.Text(
            "Время на каждом уровне:",
            self.window.width // 2,
            self.window.height * 0.55,
            arcade.color.LIGHT_BLUE,
            28,
            anchor_x="center",
            anchor_y="center"
        )

        self.level_texts = []
        start_y = self.window.height * 0.48
        row_height = 35

        for i in range(10):  # Максимум 10 уровней
            y_pos = start_y - (i * row_height)
            row_color = arcade.color.LIGHT_GRAY if i % 2 == 0 else arcade.color.WHITE

            level_text = arcade.Text(
                "",
                self.window.width // 2,
                y_pos,
                row_color,
                24,
                anchor_x="center",
                anchor_y="center"
            )
            self.level_texts.append(level_text)

        self.avg_time_text = arcade.Text(
            "",
            self.window.width // 2,
            self.window.height * 0.1,
            arcade.color.GREEN,
            24,
            anchor_x="center",
            anchor_y="center"
        )

        # Кнопка настроек
        self.settings_button = UIFlatButton(
            text="Выйти в главное меню",
            width=self.window.width * 0.25,
            height=self.window.height * 0.1,
            style=self.button_style
        )
        self.settings_button.on_click = lambda x: self.open_settings()
        self.manager.add(self.settings_button)

        # Центрируем кнопку
        button_x = self.window.width // 2 - self.settings_button.width // 2
        button_y = self.window.height * 0.15
        self.settings_button.rect = self.settings_button.rect.move(button_x, button_y)

    def on_draw(self):
        self.clear()

        # Фон победы
        arcade.draw_lbwh_rectangle_filled(
            0, 0,
            self.window.width,
            self.window.height,
            arcade.color.DARK_BLUE
        )

        # Отображаем текст
        self.title_text.draw()
        self.subtitle_text.draw()
        self.total_time_text.draw()
        self.table_title.draw()

        # Обновляем и отображаем время для каждого уровня
        sorted_times = sorted(self.level_times.items())
        for i, (level, level_time) in enumerate(sorted_times):
            if i < len(self.level_texts):
                self.level_texts[i].text = f"Уровень {level}: {level_time:.1f} сек"
                self.level_texts[i].draw()

        # Среднее время на уровень
        if self.level_times:
            avg_time = self.total_time / len(self.level_times)
            self.avg_time_text.text = f"Среднее время на уровень: {avg_time:.1f} сек"
            self.avg_time_text.draw()

        self.manager.draw()

    def open_settings(self):
        global TOTAL_GAME_TIME, LEVEL_TIMES, GLOBAL_MAP_STATE
        TOTAL_GAME_TIME = 0
        LEVEL_TIMES = {}
        GLOBAL_MAP_STATE = {
            'player_cities': [0, 1, 2],  # Начальные города игрока
            'cities_data': [],
            'selected_city_index': None
        }
        self.open_scene(StartMenu())
