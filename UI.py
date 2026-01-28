import arcade
from arcade.gui import UIFlatButton, UIBoxLayout, UIAnchorLayout, UIManager, UISlider
from pyglet.graphics import Batch
import main


class UI(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = UIManager()
        self.batch = Batch()
        self.custom_font = 'CGXYZ LCD'
        self.button_style = {
            "normal": {"font_size": 13, "font_name": self.custom_font},
            "hover": {"font_size": 13, "font_name": self.custom_font},
            "press": {"font_size": 13, "font_name": self.custom_font},
            "disabled": {"font_size": 13, "font_name": self.custom_font},
        }
        self.button_click_sound = arcade.load_sound("resources/sounds/button-click.mp3")

    def on_draw(self):
        self.clear()
        self.batch.draw()
        self.manager.draw()

    def open_scene(self, scene):
        self.manager.disable()
        arcade.play_sound(self.button_click_sound)
        self.window.show_view(scene)
        scene.manager.enable()


class StartMenu(UI):
    def __init__(self):
        super().__init__()
        self.manager.enable()
        self.menu_text = arcade.Text("Подводная битва", self.window.width / 2, self.window.height * 0.75,
                                     arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch,
                                     font_name=self.custom_font)
        self.background_color = arcade.color.BLUE_GRAY  # Фон для меню
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        start_button = UIFlatButton(text="Начать игру", width=450, height=100, color=arcade.color.BLUE,
                                    style=self.button_style)
        start_button.on_click = lambda event: self.open_scene(SelectGame())

        settings_button = UIFlatButton(text="Настройки", width=450, height=100, color=arcade.color.BLUE,
                                       style=self.button_style)
        settings_button.on_click = lambda event: self.open_scene(GameSettins())
        exit_button = UIFlatButton(text="Выйти из игры", width=450, height=100, color=arcade.color.BLUE,
                                   style=self.button_style)
        exit_button.on_click = lambda event: arcade.close_window()

        self.box_layout.add(start_button)
        self.box_layout.add(settings_button)
        self.box_layout.add(exit_button)


class SelectGame(UI):
    def __init__(self):
        super().__init__()
        self.menu_text = arcade.Text("Выбор режима игры", self.window.width / 2, self.window.height * 0.75,
                                     arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch,
                                     font_name=self.custom_font)
        self.background_color = arcade.color.BLUE_GRAY  # Фон для меню
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        start_button = UIFlatButton(text="Начать новую игру", width=450, height=100, color=arcade.color.BLUE,
                                    style=self.button_style)
        start_button.on_click = lambda x: self.open_scene(main.Game.GlobalMain())

        load_button = UIFlatButton(text="Загрузить сохранение", width=450, height=100, color=arcade.color.BLUE,
                                   style=self.button_style)
        load_button.on_click = lambda event: print("Flat клик!")

        return_button = UIFlatButton(text="Вернуться в меню", width=450, height=100, color=arcade.color.BLUE,
                                     style=self.button_style)
        return_button.on_click = lambda x: self.open_scene(StartMenu())

        self.box_layout.add(start_button)
        self.box_layout.add(load_button)
        self.box_layout.add(return_button)


class GameSettins(UI):
    def __init__(self):
        super().__init__()
        self.menu_text = arcade.Text("Настройки", self.window.width / 2, self.window.height * 0.75,
                                     arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        self.background_color = arcade.color.BLUE_GRAY  # Фон для меню
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        return_button = UIFlatButton(text="Вернуться", width=450, height=100, color=arcade.color.BLUE,
                                     style=self.button_style)
        return_button.on_click = lambda x: self.open_scene(SelectGame())
        slider = UISlider(width=400, height=50, min_value=0, max_value=100, value=50)
        slider.on_change = lambda value: print(f"Слайдер: {value}")
        self.box_layout.add(slider)
        self.box_layout.add(return_button)


class GameMenu(UI):
    pass
