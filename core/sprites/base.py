import arcade

from pathlib import Path
from typing import List, Union

from core import config


def load_textures_from_path(subfolder: Union[str, Path]) -> List[arcade.Texture]:
    folder = config.SPRITES_PATH.joinpath(subfolder)
    return [
        arcade.load_texture(str(image))
        for image in sorted(folder.glob('*.png'))
    ]
