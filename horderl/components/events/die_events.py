from abc import ABC, abstractmethod
from dataclasses import dataclass

from engine import constants
from engine.components.component import Component


@dataclass
class Die(Component):
    """
    Emitted when an entity has died.
    """

    killer: int = constants.INVALID


class DeathListener(Component, ABC):
    """
    Called when the entity dies.
    """

    @abstractmethod
    def on_die(self, scene):
        raise NotImplementedError()
