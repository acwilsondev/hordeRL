from dataclasses import dataclass

from engine.components.actor import Actor
from engine.constants import PRIORITY_MEDIUM


@dataclass
class EnergyActor(Actor):
    """
    Track scheduling metadata for actors that act on the world timeline.
    """

    INSTANT = 0
    QUARTER_HOUR = 3
    HALF_HOUR = 6
    FAST = 8
    HOURLY = 12
    VERY_SLOW = 24
    DAILY = 288

    priority: int = PRIORITY_MEDIUM
    next_turn_to_act: int = 0
    energy_cost: int = HOURLY
    is_recharging: bool = True  # True if the entity should accept energy
