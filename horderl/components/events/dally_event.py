from abc import ABC, abstractmethod
from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class DallyEvent(Component):
    """
    Emitted when the owning entity dallies.
    """


class DallyListener(Component, ABC):
    """
    Trigger when the owning entity takes a step.
    """

    @abstractmethod
    def on_dally(self, scene):
        raise NotImplementedError()
