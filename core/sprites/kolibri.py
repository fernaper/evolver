import arcade
import math
import random

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

from core import config
from .base import (
    guid, inverse_color, load_textures_from_path
)

class KolibriDiet(Enum):
    herbivore = (210, 255, 200, 0)
    carnivorous = (255, 205, 200, 0)
    sun = (255, 245, 200, 0)


class KolibriActions(Enum):
    idle = auto()
    walking = auto()
    eating = auto()
    sleeping = auto()
    dying = auto()


@dataclass
class KolibriProperties():
    spawn_time: int = field(default_factory=lambda : random.randint(250, 1000))
    max_live: int = field(default_factory=lambda : random.randint(150, 3000))
    max_speed: float = field(default_factory=lambda : random.uniform(0.2, 15))
    max_angle_speed: float = field(default_factory=lambda : random.uniform(0.1, 3.5))
    max_size: float = field(default_factory=lambda : random.uniform(0.75, 3))


@dataclass
class KolibriCounters():
    texture_counter: int = 0
    action_counter: int = 0
    spawn_counter: int = 1
    live_counter: int = 0


class KolibriSprite(arcade.Sprite):

    FRAMES_TO_UPDATE = 12
    FRAMES_TO_ACTION = 24

    def __init__(self, kolibri_list: arcade.SpriteList, center_x: Optional[int] = None, center_y: Optional[int] = None):
        super().__init__()
        self.id = guid()
        self.speed: float = 0
        self.diet = random.choice(list(KolibriDiet))
        self.action_to_textures = self.build_action_to_texture()
        self.properties = KolibriProperties()
        self.counters = KolibriCounters()
        self.__active_action = KolibriActions.idle
        self.angle = random.uniform(0, 360)
        self.center_x: int = 32 * self.properties.max_size if center_x is None else center_x
        self.center_y: int = 32 * self.properties.max_size if center_y is None else center_y
        self.scale: float = 1.5

        # Shared reference to kolibri list
        self.kolibri_list = kolibri_list
        self.kolibri_list.append(self)
        #print(f'Spawned #{self.id}')

    def build_action_to_texture(self):
        action_to_textures = {
            KolibriActions.idle: load_textures_from_path('kolibri/idle/'),
            KolibriActions.walking: load_textures_from_path('kolibri/walking/'),
            KolibriActions.eating: load_textures_from_path('kolibri/eating/'),
            KolibriActions.sleeping: load_textures_from_path('kolibri/sleeping/'),
            KolibriActions.dying: load_textures_from_path('kolibri/dying/'),
        }

        kolibri_color = inverse_color(self.diet.value)
        final_action_to_textures = {}
        for action, textures in action_to_textures.items():
            final_action_to_textures[action] = []
            for i, texture in enumerate(textures):
                final_image = []
                for pixel in texture.image.getdata():
                    pixel = [
                        max(component - kolibri_color[j], 0)
                        for j, component in enumerate(pixel)
                    ]
                    final_image.append(tuple(pixel))

                final_action_to_textures[action].append(
                    arcade.Texture.create_empty(
                        f'{action.name}_{i}_{kolibri_color}',
                        (64,64)
                    )
                )
                final_action_to_textures[action][-1].image.putdata(final_image)

        return final_action_to_textures

    @property
    def action(self):
        return self.__active_action

    @action.setter
    def action(self, action: KolibriActions) -> None:
        if action == self.__active_action:
            return
        self.__active_action = action
        self.counters.texture_counter = 0

    def update(self):
        self.update_scale()
        self.update_action()

        if self.action == KolibriActions.walking:
            self.speed = self.properties.max_speed
        else:
            self.speed = 0

        if self.action not in (KolibriActions.sleeping, KolibriActions.eating, KolibriActions.dying):
            self.change_angle = self.properties.max_angle_speed * random.choice([1,-1])
            if self.counters.spawn_counter % self.properties.spawn_time == 0:
                self.spawn_child()

        # Convert angle in degrees to radians.
        angle_rad = math.radians(self.angle)
        self.angle += self.change_angle
        # Use math to find our change based on our speed and angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)

        self.update_animation()
        self.update_counters()

    def update_scale(self):
        self.scale = max(
            self.properties.max_size / 2,
            min(
                self.properties.max_size,
                self.properties.max_size * (self.counters.live_counter / (self.properties.spawn_time / 3))
            )
        )

    def update_action(self):
        if self.counters.live_counter >= self.properties.max_live:
            if self.action != KolibriActions.dying:
                self.action = KolibriActions.dying
            return
        self.counters.action_counter = self.counters.action_counter % KolibriSprite.FRAMES_TO_ACTION
        if self.counters.action_counter == 0:
            self.action = random.choice([KolibriActions.walking, KolibriActions.idle])

    def update_animation(self):
        textures = self.action_to_textures[self.__active_action]
        frame = self.counters.texture_counter // KolibriSprite.FRAMES_TO_UPDATE
        if frame >= len(textures):
            frame = 0
            self.counters.texture_counter = 0
            if self.__active_action == KolibriActions.dying:
                print(f'Die #{self.id}')
                self.remove_from_sprite_lists()
                return
        self.texture = textures[frame]
        #print(self.action, '---->', self.counters.action_counter)

    def spawn_child(self) -> 'KolibriSprite':
        return KolibriSprite(self.kolibri_list, self.center_x, self.center_y)

    def reset_counters(self):
        self.counters.texture_counter += 0
        self.counters.action_counter += 0
        self.counters.spawn_counter += 0

    def update_counters(self):
        self.counters.texture_counter += 1
        self.counters.action_counter += 1
        self.counters.spawn_counter += 1
        self.counters.live_counter += 1
