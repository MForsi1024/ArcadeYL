import arcade
from arcade.gui import UIFlatButton, UIBoxLayout, UIAnchorLayout, UIManager
from pyglet.graphics import Batch

class UI(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = UIManager()
        self.manager.enable()
        self.background_color = arcade.color.BLUE_GRAY  # Фон для меню
        self.batch = Batch()

    def on_draw(self):
        self.clear()
        self.batch.draw()
        self.manager.draw()


class StartMenu(UI):
    def __init__(self):
        super().__init__()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        self.flat_button = UIFlatButton(text="Плоская Кнопка", width=200, height=50, color=arcade.color.BLUE)
        self.flat_button.on_click = lambda event: print("Flat клик!")  # Не только лямбду, конечно
        self.box_layout.add(self.flat_button)


class GameMenu(UI):
    pass


if __name__ == '__main__':
    window = arcade.Window(800, 600, "Учимся ставить на паузу")
    menu_view = UI()
    window.show_view(menu_view)
    arcade.run()
