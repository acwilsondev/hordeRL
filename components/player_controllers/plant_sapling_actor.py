from dataclasses import dataclass
from typing import Tuple, List

from components.player_controllers.place_thing_actor import PlaceThingActor
from content.terrain.saplings import make_sapling
from engine.component import Component


@dataclass
class PlaceSaplingActor(PlaceThingActor):
    gold_cost: int = 1

    def make_thing(self, x: int, y: int) -> Tuple[int, List[Component]]:
        return make_sapling(x, y)
