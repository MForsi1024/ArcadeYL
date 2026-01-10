import arcade
from arcade.gui import UIFlatButton, UIBoxLayout, UIAnchorLayout, UIManager
from pyglet.graphics import Batch


class UI(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = UIManager()
        self.manager.enable()
        self.batch = Batch()

    def on_draw(self):
        self.clear()
        self.batch.draw()
        self.manager.draw()


class StartMenu(UI):
    def __init__(self):
        super().__init__()
        self.menu_text = arcade.Text("Подводная битва", self.window.width / 2, self.window.height * 0.75,
                                     arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        self.background_color = arcade.color.BLUE_GRAY  # Фон для меню
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        button_style = {
            "normal": {"font_size": 25},
            "hover": {"font_size": 25},
            "press": {"font_size": 25},
            "disabled": {"font_size": 25}
        }

        start_button = UIFlatButton(text="Начать игру", width=450, height=100, color=arcade.color.BLUE, style=button_style)
        start_button.on_click = lambda event: print("Flat клик!")

        settings_button = UIFlatButton(text="Настройки", width=450, height=100, color=arcade.color.BLUE, style=button_style)
        settings_button.on_click = lambda event: print("Flat клик!")

        exit_button = UIFlatButton(text="Выйти из игры", width=450, height=100, color=arcade.color.BLUE, style=button_style)
        exit_button.on_click = lambda event: arcade.close_window()

        self.box_layout.add(start_button)
        self.box_layout.add(settings_button)
        self.box_layout.add(exit_button)

    def on_draw(self):
        super().on_draw()


class GameMenu(UI):
    pass


if __name__ == '__main__':
    print(arcade.get_display_size())
    width, height = arcade.get_display_size()
    window = arcade.Window(
        width=width,
        height=height,
        title="Подводная битва")
    window.set_location(0, 0)
    menu_view = StartMenu()
    window.show_view(menu_view)
    arcade.run()
