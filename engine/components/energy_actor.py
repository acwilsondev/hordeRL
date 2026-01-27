from dataclasses import dataclass

from engine.components.actor import Actor
from engine.constants import PRIORITY_MEDIUM


@dataclass
class EnergyActor(Actor):
    """
    Provides control and other 'mind' information.
    """

    INSTANT = 0
    QUARTER_HOUR = 3
    HALF_HOUR = 6
    FAST = 8
    HOURLY = 12
    VERY_SLOW = 24
    DAILY = 288

    priority: int = PRIORITY_MEDIUM
    energy: int = 0
    energy_cost: int = HOURLY
    is_recharging: bool = True  # True if the entity should accept energy
    current_turn: int = 0
    next_turn_to_act: int = 0

    def __post_init__(self) -> None:
        if self.current_turn != 0 or self.next_turn_to_act != 0:
            self.energy = self.current_turn - self.next_turn_to_act
            return
        if self.energy != 0:
            self.next_turn_to_act = self.current_turn - self.energy
