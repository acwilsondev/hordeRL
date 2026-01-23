from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class WorldTurns(Component):
    """Track the current world turn count."""

    current_turn: int = 0
