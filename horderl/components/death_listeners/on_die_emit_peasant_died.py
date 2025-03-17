from dataclasses import dataclass

from horderl.components.events.die_events import DeathListener
from horderl.components.events.peasant_events import PeasantDied
from horderl.engine import core


@dataclass
class OnDieEmitPeasantDied(DeathListener):
    """
    Translate a peasant death into a population count decrement.
    """

    def on_die(self, scene):
        scene.cm.add(PeasantDied(entity=core.get_id("world")))
