from dataclasses import dataclass

from horderl.components.brains.brain import Brain
from horderl.components.events.attack_started_events import AttackStartListener


@dataclass
class FastForwardBrain(Brain, AttackStartListener):
    """
    Brain that fast-forwards time until interrupted.

    This brain defers logic to brain systems and only stores state.
    """

    def on_attack_start(self, scene):
        from horderl.systems.brain_system import on_fast_forward_attack_start

        on_fast_forward_attack_start(scene, self)
