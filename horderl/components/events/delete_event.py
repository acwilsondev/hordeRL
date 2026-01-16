from abc import ABC, abstractmethod
from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class Delete(Component):
    """
    Add this to an entity to have it delete itself after some time.
    """

    next_update: int = 0


@dataclass
class DeleteListener(Component, ABC):
    """
    A world building step.
    """

    @abstractmethod
    def on_delete(self, scene):
        raise NotImplementedError()
