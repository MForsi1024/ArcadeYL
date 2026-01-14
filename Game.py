import arcade
from arcade.gui import UIFlatButton, UIBoxLayout, UIAnchorLayout, UIManager, UISlider
from pyglet.graphics import Batch
from UI import UI

class GlobalMain(UI):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_image("resources/images/arcade_test_background.png")