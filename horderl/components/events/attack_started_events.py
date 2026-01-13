from abc import ABC, abstractmethod
from dataclasses import dataclass

from engine.components.component import Component
from engine.components.events import Event


class AttackStartListener(Component, ABC):
    """
    Define a step to take when an attack starts.
    """

    @abstractmethod
    def on_attack_start(self, scene):
        raise NotImplementedError()


@dataclass
class AttackStarted(Event):
    """
    Emitted when the attack should begin.
    """

    def listener_type(self):
        return AttackStartListener

    def notify(self, scene, listener):
        listener.on_attack_start(scene)
