from dataclasses import dataclass

from horderl.components.events.new_day_event import DayBeganListener


@dataclass
class GrowIntoTree(DayBeganListener):
    """Track saplings that should grow into trees after enough warm days."""

    time_to_grow: int = 0
