import arcade
from pyglet.graphics import Batch

class UI(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLUE_GRAY  # Фон для меню

        self.batch = Batch()
        self.main_text = arcade.Text("Главное Меню", self.window.width / 2, self.window.height / 2 + 50,
                                     arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Нажми SPACE, чтобы начать!", self.window.width / 2, self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)


    def on_draw(self):
        self.clear()
        self.batch.draw()


class StartMenu(UI):
    pass


class GameMenu(UI):
    pass

if __name__ == '__main__':
    window = arcade.Window(800, 600, "Учимся ставить на паузу")
    menu_view = UI()
    window.show_view(menu_view)
    arcade.run()