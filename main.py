import arcade

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

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        self.kolibri_list = arcade.SpriteList()
        self.kolibri_list.append(KolibriSprite())

    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()
        for kolibri_sprite in self.kolibri_list:
            kolibri_sprite.draw(pixelated=True)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.kolibri_list.update()
        self.kolibri_list.update_animation(delta_time)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.UP or key == arcade.key.W:
            for k in self.kolibri_list:
                k.speed = 8
        elif key == arcade.key.DOWN or key == arcade.key.S:
            for k in self.kolibri_list:
                k.speed = -8
        elif key == arcade.key.LEFT or key == arcade.key.A:
            for k in self.kolibri_list:
                k.change_angle = 2
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            for k in self.kolibri_list:
                k.change_angle = -2
        elif key == arcade.key.SPACE:
            self.kolibri_list.append(KolibriSprite())

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP or key == arcade.key.W:
            for k in self.kolibri_list:
                k.speed = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            for k in self.kolibri_list:
                k.speed = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            for k in self.kolibri_list:
                k.change_angle = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            for k in self.kolibri_list:
                k.change_angle = 0

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
