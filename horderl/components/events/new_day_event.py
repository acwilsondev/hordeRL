from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class DayBegan(Component):
    """
    Add this to an entity to have it delete itself after some time.
    """

    day: int = 0


@dataclass
class DayBeganListener(Component):
    """
    A world building step.
    """
