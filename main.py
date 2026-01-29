import Game
import UI
import Saves
import arcade

from Saves import FileManager

audio = 50
file_manager = FileManager('resources/saves/saves.txt')
def get_audio_volume():
    pass


def main():

    width, height = arcade.get_display_size()
    window = arcade.Window(
        width=width,
        height=height,
        title="Подводная битва")
    window.set_location(0, 0)
    menu_view = UI.StartMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == '__main__':
    Main().main()
