import arcade
import random

from pyglet.math import Vec2

from core import config
from core.sprites.kolibri import KolibriSprite


SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
CAMERA_SPEED = 0.99
STARTING_KOLIBRIS = 100
SCREEN_TITLE = 'Evolver'


class Evolver(arcade.Window):

    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.AMAZON)
        self.kolibri_list = None
        self.current_position = [0, 0]
        self.move_camera = [0,0]
        self.camera_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)


    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        self.kolibri_list = arcade.SpriteList()

        for _ in range(STARTING_KOLIBRIS):
            KolibriSprite(
                self.kolibri_list,
                center_x=random.randint(0, SCREEN_WIDTH),
                center_y=random.randint(0, SCREEN_HEIGHT)
            )

    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()
        self.draw_sprites()
        self.draw_gui()

    def draw_sprites(self):
        self.camera_sprites.use()
        for kolibri_sprite in self.kolibri_list:
            kolibri_sprite.draw(pixelated=True)

    def draw_gui(self):
        self.camera_gui.use()
        arcade.draw_rectangle_filled(
            self.width // 2, 20, self.width, 40, arcade.color.ALMOND
        )
        text = (
            f'Scroll value: ({self.camera_sprites.position[0]:5.1f}, '
            f'{self.camera_sprites.position[1]:5.1f}); Alive: {len(self.kolibri_list)}'
        )
        arcade.draw_text(text, 10, 10, arcade.color.BLACK_BEAN, 20)


    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.kolibri_list.update()
        # Scroll the screen to the player
        self.scroll_to_position()

    def scroll_to_position(self):
        self.current_position[0] += self.move_camera[0]
        self.current_position[1] += self.move_camera[1]
        self.camera_sprites.move_to(Vec2(*self.current_position), CAMERA_SPEED)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.UP or key == arcade.key.W:
            self.move_camera[1] = 10
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.move_camera[1] = -10
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.move_camera[0] = -10
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.move_camera[0] = 10
        elif key == arcade.key.SPACE:
            self.kolibri_list.append(KolibriSprite())

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP or key == arcade.key.W:
            self.move_camera[1] = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.move_camera[1] = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.move_camera[0] = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.move_camera[0] = 0

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
    game = Evolver(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    game.set_update_rate(1 / 60)
    arcade.run()


if __name__ == "__main__":
    main()
