from abc import ABC, abstractmethod
from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class AttackFinished(Component):
    """
    Emitted after an entity's attack has been processed.
    """


@dataclass
class OnAttackFinishedListener(Component, ABC):
    """
    Respond to completed attacks.
    """

    @abstractmethod
    def on_attack_finished(self, scene, caller):
        raise NotImplementedError()
