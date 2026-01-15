from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class Flooder(Component):
    """
    Mark an entity as a source of flood filling, with optional cooldown data.
    """

    next_flood_time_ms: int = 0
    flood_interval_ms: int = 500
