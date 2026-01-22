from dataclasses import dataclass

from ..components.events.attack_events import OnAttackFinishedListener


@dataclass
class DieOnAttackFinished(OnAttackFinishedListener):
    """Tag entities that should die after they finish an attack."""
