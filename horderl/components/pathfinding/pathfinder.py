from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class Pathfinder(Component):
    """Data-only component indicating an entity can request pathfinding."""

    diagonal: int = 3
