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
        start_button = UIFlatButton(text="Начать игру", width=200, height=50, color=arcade.color.BLUE)
        start_button.on_click = lambda x: self.window.show_view(SelectGame())

        settings_button = UIFlatButton(text="Настройки", width=200, height=50, color=arcade.color.BLUE)
        settings_button.on_click = print

        exit_button = UIFlatButton(text="Выйти из игры", width=200, height=50, color=arcade.color.BLUE)
        exit_button.on_click = lambda event: arcade.close_window()

        self.box_layout.add(start_button)
        self.box_layout.add(settings_button)
        self.box_layout.add(exit_button)


class SelectGame(UI):
    def __init__(self):
        super().__init__()
        self.menu_text = arcade.Text("Выбор режима игры", self.window.width / 2, self.window.height * 0.75,
                                     arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        self.background_color = arcade.color.BLUE_GRAY  # Фон для меню
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        start_button = UIFlatButton(text="Начать новую игру", width=200, height=50, color=arcade.color.BLUE)
        start_button.on_click = lambda event: print("Flat клик!")

        load_button = UIFlatButton(text="Загрузить сохранение", width=200, height=50, color=arcade.color.BLUE)
        load_button.on_click = lambda event: print("Flat клик!")

        return_button = UIFlatButton(text="Вернуться в меню", width=200, height=50, color=arcade.color.BLUE)
        return_button.on_click = lambda x: self.window.show_view(StartMenu())

        self.box_layout.add(start_button)
        self.box_layout.add(load_button)
        self.box_layout.add(return_button)


class GameSettins(UI):
    pass


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
