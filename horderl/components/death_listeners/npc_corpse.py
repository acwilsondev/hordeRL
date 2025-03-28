from dataclasses import dataclass

from horderl.components import Coordinates
from horderl.components.events.die_events import DeathListener
from horderl.content import corpses
from horderl.engine import palettes
from horderl.engine.components.entity import Entity


@dataclass
class Corpse(DeathListener):
    symbol: str = "%"
    color: tuple = palettes.BLOOD
    bg_color: tuple = palettes.BACKGROUND

    def on_die(self, scene):
        self._log_info("spawned a corpse")
        entity_obj = scene.cm.get_one(Entity, entity=self.entity)
        coords = scene.cm.get_one(Coordinates, entity=self.entity)

        splatter = corpses.make_blood_splatter(
            5, coords.x, coords.y, self.color
        )
        if splatter:
            scene.cm.add(*splatter)
        scene.cm.add(
            *corpses.make_corpse(
                name=entity_obj.name,
                symbol=self.symbol,
                x=coords.x,
                y=coords.y,
                color=self.color,
            )[1]
        )
