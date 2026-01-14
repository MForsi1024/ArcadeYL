import arcade
from arcade.gui import UIFlatButton, UIBoxLayout, UIAnchorLayout, UIManager, UISlider
from pyglet.graphics import Batch
from UI import UI

class GlobalMain(UI):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("resources/images/arcade_test_background.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.rect.XYWH(self.width // 2, self.height // 2, self.width, self.height,), pixelated=True
        )
