from abc import ABC, abstractmethod
from dataclasses import dataclass

from engine.components.component import Component


class AttackStartListener(Component, ABC):
    """
    Define a step to take when an attack starts.
    """

    @abstractmethod
    def on_attack_start(self, scene):
        raise NotImplementedError()


@dataclass
class AttackStarted(Component):
    """
    Emitted when the attack should begin.
    """
