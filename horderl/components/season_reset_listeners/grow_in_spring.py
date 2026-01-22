import random
from dataclasses import dataclass, field

from horderl.components.events.new_day_event import DayBeganListener


def temperature_time_to_grow():
    return random.randint(1200, 3600)


@dataclass
class GrowIntoTree(DayBeganListener):
    """Track saplings that should grow into trees after enough warm days."""

    time_to_grow: int = field(default_factory=temperature_time_to_grow)
