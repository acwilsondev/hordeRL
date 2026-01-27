from dataclasses import dataclass
from typing import Optional, Union

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

    def can_act(self, current_turn: Union[int, object]) -> bool:
        """
        Return whether the actor is ready to act based on turn tracking.

        Args:
            current_turn: Current world turn value, or an object with a
                ``current_turn`` attribute.

        Returns:
            True when the current turn has reached or exceeded the scheduled
            turn to act; otherwise False.
        """
        # Use >= so actors can act the moment they reach their scheduled turn.
        return (
            self._resolve_current_turn(current_turn) >= self.next_turn_to_act
        )

    def pass_turn(
        self, current_turn: Union[int, object], time: Optional[int] = None
    ) -> None:
        """
        Advance the actor's schedule by consuming a turn cost.

        Args:
            current_turn: Current world turn value, or an object with a
                ``current_turn`` attribute.
            time: Optional override for the number of turns to wait before the
                next action. Defaults to ``energy_cost``.

        Side Effects:
            - Updates ``next_turn_to_act`` for readiness checks.
        """
        if time is None:
            time = self.energy_cost
        self.next_turn_to_act = self._resolve_current_turn(current_turn) + time

    @staticmethod
    def _resolve_current_turn(current_turn: Union[int, object]) -> int:
        # Accept world turn objects without importing higher-level modules.
        if hasattr(current_turn, "current_turn"):
            return int(getattr(current_turn, "current_turn"))
        return int(current_turn)
