from dataclasses import dataclass

from engine import constants
from engine.components.component import Component


@dataclass
class Stomach(Component):
    """Track an entity stored inside another entity."""

    contents: int = constants.INVALID
