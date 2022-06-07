import arcade
import math

from enum import Enum, auto
from pathlib import Path

from core import config
from .base import load_textures_from_path


class KolibriActions(Enum):
    idle = auto()
    walking = auto()
    eating = auto()
    sleeping = auto()
    dying = auto()


class KolibriSprite(arcade.Sprite):

    FRAMES_TO_UPDATE = 12

    def __init__(self):
        super().__init__()
        self.scale: float = 4
        self.speed: float = 0
        self.center_x: int = 32 * self.scale
        self.center_y: int = 32 * self.scale

        self.action_to_textures = {
            KolibriActions.idle: load_textures_from_path('kolibri/idle/'),
            KolibriActions.walking: load_textures_from_path('kolibri/walking/'),
            KolibriActions.eating: load_textures_from_path('kolibri/eating/'),
            KolibriActions.sleeping: load_textures_from_path('kolibri/sleeping/'),
            KolibriActions.dying: load_textures_from_path('kolibri/dying/'),
        }

        self.__active_action = KolibriActions.idle
        self.__texture_counter = 0

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, action: KolibriActions) -> None:
        if action == self.__active_action:
            return
        self.__active_action = action
        self.__texture_counter = 0

    def update(self):
        # Convert angle in degrees to radians.
        angle_rad = math.radians(self.angle)
        # Rotate
        self.angle += self.change_angle
        # Use math to find our change based on our speed and angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)

        if self.speed != 0:
            self.action = KolibriActions.walking
        else:
            self.action = KolibriActions.idle

    def update_animation(self, delta_time: float = 1 / 60):
        textures = self.action_to_textures[self.__active_action]
        self.__texture_counter += 1
        if self.__texture_counter >= len(textures) * KolibriSprite.FRAMES_TO_UPDATE:
            self.__texture_counter = 0
        frame = self.__texture_counter // KolibriSprite.FRAMES_TO_UPDATE
        self.texture = textures[frame]
