import arcade

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
        self.scale = 0.5
        self.center_x = 32 * self.scale
        self.center_y = 32 * self.scale

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

    @property
    def action(self, action: KolibriActions) -> None:
        self.__active_action = action
        self.__texture_counter = 0

    def update_animation(self, delta_time: float = 1 / 60):
        textures = self.action_to_textures[self.__active_action]
        self.__texture_counter += 1
        if self.__texture_counter >= len(textures) * KolibriSprite.FRAMES_TO_UPDATE:
            self.__texture_counter = 0
        frame = self.__texture_counter // KolibriSprite.FRAMES_TO_UPDATE
        self.texture = textures[frame]
