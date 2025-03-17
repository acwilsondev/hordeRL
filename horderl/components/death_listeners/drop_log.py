from dataclasses import dataclass

from horderl.components import Coordinates
from horderl.components.events.die_events import DeathListener
from horderl.content.getables.fallen_log import make_fallen_log


@dataclass
class DropFallenLog(DeathListener):
    """Drop gold when the owner dies."""

    def on_die(self, scene):
        self._log_info("dropped a log on death")
        coords = scene.cm.get_one(Coordinates, entity=self.entity)
        scene.cm.add(*make_fallen_log(coords.x, coords.y)[1])
