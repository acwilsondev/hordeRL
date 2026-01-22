import random
from dataclasses import dataclass

from horderl.components.events.new_day_event import DayBeganListener


def make_grow_into_tree(entity: int) -> "GrowIntoTree":
    """Create a GrowIntoTree component with a randomized grow timer.

    Args:
        entity: Entity ID that will own the component.

    Returns:
        GrowIntoTree: Component with time_to_grow initialized.

    Side Effects:
        - None.
    """

    return GrowIntoTree(entity=entity, time_to_grow=random.randint(1200, 3600))


@dataclass
class GrowIntoTree(DayBeganListener):
    """Track saplings that should grow into trees after enough warm days."""

    time_to_grow: int = 0
