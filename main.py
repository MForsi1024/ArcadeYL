import Game
import UI
import Saves
import arcade

if __name__ == '__main__':
    print(arcade.get_display_size())
    width, height = arcade.get_display_size()
    window = arcade.Window(
        width=width,
        height=height,
        title="Подводная битва")
    window.set_location(0, 0)
    menu_view = UI.StartMenu()
    window.show_view(menu_view)
    arcade.run()