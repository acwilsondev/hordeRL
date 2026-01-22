from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Union

from engine.components.component import Component
from horderl import palettes

Color = Tuple[int, int, int]
PaletteColor = Union[Color, str]


@dataclass
class Appearance(Component):
    """
    Define an entity's base appearance.
    """

    class RenderMode(str, Enum):
        NORMAL = "NORMAL"
        HIGH_VEE = "HIGH_VEE"
        STEALTHY = "STEALTHY"

    symbol: str = " "
    color: PaletteColor = palettes.WHITE
    bg_color: PaletteColor = palettes.BACKGROUND
    render_mode: RenderMode = RenderMode.NORMAL
