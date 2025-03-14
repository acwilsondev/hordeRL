from abc import ABC, abstractmethod
from dataclasses import dataclass

from ...components.base_components.component import Component
from ...components.base_components.events import Event
from ...engine import constants


@dataclass
class Die(Event):
    killer: int = constants.INVALID

    def listener_type(self):
        return DeathListener

    def notify(self, scene, listener):
        if listener.entity == self.entity:
            listener.on_die(scene)

    def _after_notify(self, scene):
        scene.cm.delete(self.entity)


class DeathListener(Component, ABC):
    """Called when the entity dies."""

    @abstractmethod
    def on_die(self, scene):
        raise NotImplementedError()
