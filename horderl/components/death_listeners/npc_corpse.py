from dataclasses import dataclass

from engine.components.component import Component
from horderl import palettes


@dataclass
class Corpse(Component):
    """Configure NPC corpse appearance spawned on death."""

    symbol: str = "%"
    color: tuple = palettes.BLOOD
    bg_color: tuple = palettes.BACKGROUND
