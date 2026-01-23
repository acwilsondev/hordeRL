from dataclasses import dataclass
from typing import Optional

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

    def can_act(self) -> bool:
        """
        Return whether the actor is ready to act based on turn tracking.

        Returns:
            True when the current turn has reached or exceeded the scheduled
            turn to act; otherwise False.
        """
        # Use >= so actors can act the moment they reach their scheduled turn.
        return self.current_turn >= self.next_turn_to_act

    def pass_turn(self, time: Optional[int] = None) -> None:
        """
        Advance the actor's schedule by consuming a turn cost.

        Args:
            time: Optional override for the number of turns to wait before the
                next action. Defaults to ``energy_cost``.

        Side Effects:
            - Updates ``next_turn_to_act`` and ``energy`` for readiness checks.
        """
        if time is None:
            time = self.energy_cost
        self.next_turn_to_act = self.current_turn + time
        self.energy = self.current_turn - self.next_turn_to_act
