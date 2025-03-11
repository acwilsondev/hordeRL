from abc import ABC, abstractmethod
from dataclasses import dataclass

from components.base_components.component import Component
from components.base_components.events import Event


class AttackStartListener(Component, ABC):
    """Define a step to take when an attack starts."""

    @abstractmethod
    def on_attack_start(self, scene):
        raise NotImplementedError()


@dataclass
class AttackStarted(Event):
    """Emitted when the attack should begin."""

    def listener_type(self):
        return AttackStartListener

    def notify(self, scene, listener):
        listener.on_attack_start(scene)
