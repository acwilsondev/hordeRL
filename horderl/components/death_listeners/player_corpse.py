from dataclasses import dataclass

from engine.components.component import Component
from horderl import palettes


@dataclass
class PlayerCorpse(Component):
    """Configure the player corpse spawned on death."""

    symbol: str = "%"
    color: tuple = palettes.BLOOD
    bg_color: tuple = palettes.BACKGROUND
