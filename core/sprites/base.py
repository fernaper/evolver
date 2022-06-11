import arcade
import functools
import random
import uuid

from pathlib import Path
from typing import List, Tuple, Union

from core import config

def guid():
    return uuid.uuid4().hex[:8]


@functools.lru_cache
def load_textures_from_path(subfolder: Union[str, Path], can_cache=True) -> List[arcade.Texture]:
    folder = config.SPRITES_PATH.joinpath(subfolder)
    return [
        arcade.load_texture(str(image), can_cache=can_cache)
        for image in sorted(folder.glob('*.png'))
    ]


def generate_random_color(alpha = 0) -> Tuple[int, int, int, float]:
    return (
        random.randrange(0,255),
        random.randrange(0,255),
        random.randrange(0,255),
        alpha
    )

def inverse_color(color: Tuple[int, int, int, float]) -> Tuple[int, int, int, float]:
    return (
        255 - color[0],
        255 - color[1],
        255 - color[2],
        color[3],
    )
