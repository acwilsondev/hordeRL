from dataclasses import dataclass
from typing import Tuple

from engine import constants
from engine.components.component import Component


@dataclass
class StepEvent(Component):
    """
    Emitted when the owning entity takes a step.
    """

    new_location: Tuple[int, int] = (-1, -1)


class StepListener(Component):
    """
    Marker component for entities that react to step events.
    """

    pass


@dataclass
class EnterEvent(Component):
    """
    Emitted when the owning entity steps on another entity (if that entity cares).
    """

    entered: int = constants.INVALID


class EnterListener(Component):
    """
    Marker component for entities that react to enter events.
    """

    pass
