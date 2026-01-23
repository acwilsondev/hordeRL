from dataclasses import dataclass

from horderl.components.brains.brain import Brain
from horderl.components.events.attack_started_events import AttackStartListener


@dataclass
class FastForwardBrain(Brain, AttackStartListener):
    """
    Brain that fast-forwards time until interrupted.

    This brain defers logic to brain systems and only stores state.
    """

    """Data-only marker for fast-forward behavior at attack start."""
