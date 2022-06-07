import arcade

from enum import Enum, auto
from pathlib import Path
from typing import Tuple

from core import config
from core.sprites.kolibri import KolibriSprite


SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_TITLE = 'Evolver'


class MyGame(arcade.Window):

    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.AMAZON)

        self.kolibri_list = None
        self.kolibri_sprite = None
        self.physics_engine = None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        self.kolibri_list = arcade.SpriteList()
        self.kolibri_sprite = KolibriSprite()
        self.kolibri_list.append(self.kolibri_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.kolibri_sprite, None
        )

    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()
        self.kolibri_sprite.draw(pixelated=True)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.kolibri_list.update_animation(delta_time)
        self.physics_engine.update()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.UP or key == arcade.key.W:
            self.kolibri_sprite.change_y = 5
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.kolibri_sprite.change_y = -5
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.kolibri_sprite.change_x = -5
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.kolibri_sprite.change_x = 5

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP or key == arcade.key.W:
            self.kolibri_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.kolibri_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.kolibri_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.kolibri_sprite.change_x = 0

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
