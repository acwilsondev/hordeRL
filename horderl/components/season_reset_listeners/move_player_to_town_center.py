from dataclasses import dataclass

from horderl.components.events.attack_started_events import AttackStartListener


@dataclass
class MovePlayerToTownCenter(AttackStartListener):
    """Data-only marker for moving the player to the town center."""
