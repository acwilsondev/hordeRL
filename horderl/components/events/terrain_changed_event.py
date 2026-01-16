from abc import ABC, abstractmethod
from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class TerrainChangedEvent(Component):
    """
    Emitted when terrain has changed.
    """


class TerrainChangedListener(Component, ABC):
    """
    Respond to terrain changes.
    """

    @abstractmethod
    def on_terrain_changed(self, scene):
        raise NotImplementedError()
