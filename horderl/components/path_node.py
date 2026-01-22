from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class PathNode(Component):
    """Store a single step in a precomputed path for animations."""

    step: int = 0
    x: int = 0
    y: int = 0
