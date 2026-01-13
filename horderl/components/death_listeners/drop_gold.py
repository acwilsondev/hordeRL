from dataclasses import dataclass

from horderl.components import Coordinates
from horderl.components.events.die_events import DeathListener
from horderl.content.getables.gold import make_gold_nugget
from engine.logging import get_logger


@dataclass
class DropGold(DeathListener):
    """
    Drop gold when the owner dies.
    """

    def on_die(self, scene):
        get_logger(__class__).info(
            "dropped gold nugget on death",
            extra={"entity": self.entity},
        )
        coords = scene.cm.get_one(Coordinates, entity=self.entity)
        scene.cm.add(*make_gold_nugget(coords.x, coords.y)[1])
