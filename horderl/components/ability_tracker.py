from dataclasses import dataclass

from ..components.events.attack_started_events import AttackStartListener


@dataclass
class AbilityTracker(AttackStartListener):
    """
    Track the currently selected ability index for an entity.

    This component only stores selection metadata; selection logic lives in
    the ability selection system.
    """

    current_ability: int = 0
