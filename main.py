import arcade

from enum import Enum, auto
from pathlib import Path
from typing import Tuple

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_TITLE = 'Evolver'


def load_texture_pair(filename: str) -> Tuple[arcade.Texture]:
    """
    Load a texture pair, with the second being a mirror image.
    """
    return (
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    )


class Direction(Enum):
    right = auto()
    left = auto()


class DinoSprite(arcade.Sprite):

    UPDATES_PER_FRAME = 7

    def __init__(self, default_path: str):
        super().__init__()
        self.scale = 2
        self.center_x = 7 * self.scale
        self.center_y = 9 * self.scale
        self.direction = Direction.right
        self.texture_index = 0
        self.idle_textures = [
            load_texture_pair(str(image))
            for image in sorted(Path(default_path).joinpath('Iddle').glob('*.png'))
        ]
        self.walk_textures = [
            load_texture_pair(str(image))
            for image in sorted(Path(default_path).joinpath('Walk').glob('*.png'))
        ]
        self.hurt_textures = [
            load_texture_pair(str(image))
            for image in sorted(Path(default_path).joinpath('Hurt').glob('*.png'))
        ]

    def update_animation(self, delta_time: float = 1 / 60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.direction == Direction.right:
            self.direction = Direction.left
        elif self.change_x > 0 and self.direction == Direction.left:
            self.direction = Direction.right

        direction_to_index = {
            Direction.right: 0,
            Direction.left: 1,
        }

        if self.change_x == 0 and self.change_y == 0:
            textures = self.idle_textures
        else:
            textures = self.walk_textures

        self.texture_index += 1
        if self.texture_index > len(textures) * DinoSprite.UPDATES_PER_FRAME:
            self.texture_index = 0

        frame = self.texture_index // DinoSprite.UPDATES_PER_FRAME
        frame = frame % len(textures)
        self.texture = textures[frame][direction_to_index[self.direction]]


class MyGame(arcade.Window):

    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.AMAZON)

        self.blue_dino_list = None
        self.blue_dino_sprite = None

        self.physics_engine = None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        self.blue_dino_list = arcade.SpriteList()

        self.blue_dino_sprite = DinoSprite('images/blue_dino/')
        self.blue_dino_list.append(self.blue_dino_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.blue_dino_sprite, None
        )

    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()
        self.blue_dino_sprite.draw(pixelated=True)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.blue_dino_list.update_animation(delta_time)
        self.physics_engine.update()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.UP or key == arcade.key.W:
            self.blue_dino_sprite.change_y = 5
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.blue_dino_sprite.change_y = -5
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.blue_dino_sprite.change_x = -5
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.blue_dino_sprite.change_x = 5

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP or key == arcade.key.W:
            self.blue_dino_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.blue_dino_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.blue_dino_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.blue_dino_sprite.change_x = 0

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
