from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class TerrainChangedOnDeath(Component):
    """
    This entity is a part of the terrain and should notify anything that cares about
    terrain when it dies.
    """
