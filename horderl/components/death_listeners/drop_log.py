from dataclasses import dataclass
from engine.components import Coordinates

from engine.logging import get_logger
from horderl.components.events.die_events import DeathListener
from horderl.content.getables.fallen_log import make_fallen_log


@dataclass
class DropFallenLog(DeathListener):
    """
    Drop gold when the owner dies.
    """

    def on_die(self, scene):
        get_logger(__class__).info(
            "dropped fallen log on death",
            extra={"entity": self.entity},
        )
        coords = scene.cm.get_one(Coordinates, entity=self.entity)
        scene.cm.add(*make_fallen_log(coords.x, coords.y)[1])
