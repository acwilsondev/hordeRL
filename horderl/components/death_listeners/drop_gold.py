from dataclasses import dataclass

from horderl.components import Coordinates
from horderl.components.events.die_events import DeathListener
from horderl.content.getables.gold import make_gold_nugget


@dataclass
class DropGold(DeathListener):
    """
    Drop gold when the owner dies.
    """

    def on_die(self, scene):
        self._log_info(f"dropped gold on death")
        coords = scene.cm.get_one(Coordinates, entity=self.entity)
        scene.cm.add(*make_gold_nugget(coords.x, coords.y)[1])
