from dataclasses import dataclass

from engine import constants
from engine.components.component import Component


@dataclass
class Die(Component):
    """
    Emitted when an entity has died.
    """

    killer: int = constants.INVALID
