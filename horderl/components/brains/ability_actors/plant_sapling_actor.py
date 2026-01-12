from dataclasses import dataclass
from typing import List, Tuple

from horderl.components.brains.ability_actors.place_thing_actor import (
    PlaceThingActor,
)
from horderl.content.terrain.saplings import make_sapling
from horderl.engine.components.component import Component


@dataclass
class PlaceSaplingActor(PlaceThingActor):
    gold_cost: int = 1

    def make_thing(self, x: int, y: int) -> Tuple[int, List[Component]]:
        return make_sapling(x, y)
