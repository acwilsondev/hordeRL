from abc import ABC, abstractmethod
from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class DayBegan(Component):
    """
    Add this to an entity to have it delete itself after some time.
    """

    day: int = 0


@dataclass
class DayBeganListener(Component, ABC):
    """
    A world building step.
    """

    @abstractmethod
    def on_new_day(self, scene, day):
        raise NotImplementedError()
