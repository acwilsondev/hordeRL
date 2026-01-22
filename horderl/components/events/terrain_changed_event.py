from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class TerrainChangedEvent(Component):
    """
    Emitted when terrain has changed.
    """


@dataclass
class TerrainChangedListener(Component):
    """
    Respond to terrain changes.
    """
