from abc import ABC, abstractmethod
from dataclasses import dataclass

from horderl.engine import constants
from horderl.engine.components.component import Component
from horderl.engine.components.events import Event


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
    """
    Called when the entity dies.
    """

    @abstractmethod
    def on_die(self, scene):
        raise NotImplementedError()
