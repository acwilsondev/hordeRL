from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class DropGold(Component):
    """Drop gold when the owner dies."""
