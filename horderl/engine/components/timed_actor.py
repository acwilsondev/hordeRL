from abc import ABC
from dataclasses import dataclass

from horderl.components.enums import ControlMode, Intention
from horderl.engine import core
from horderl.engine.components.actor import Actor
from horderl.engine.constants import PRIORITY_MEDIUM


@dataclass
class TimedActor(Actor, ABC):
    SLOWEST = 100000
    MINIMUM_FLICKER = 125
    QUARTER_HOUR = 250
    HALF_HOUR = 500
    HOURLY = 1000
    DAILY = 10000
    ONE_SECOND = 1000
    SIX_SECONDS = 6000

    REAL_TIME = 0
    """
    Provides control and other 'mind' information.
    """
    control_mode: ControlMode = None  # which system controls this entity
    priority: int = PRIORITY_MEDIUM
    timer_delay: int = HALF_HOUR
    next_update: int = 0

    # action management
    intention: Intention = Intention.NONE
    intention_target: int = None

    def can_act(self) -> bool:
        return self.next_update <= core.time_ms()

    def pass_turn(self, delay=None) -> None:
        if delay is None:
            delay = self.timer_delay
        self.next_update = core.time_ms() + delay
