from dataclasses import dataclass
from typing import List, Tuple

from ...base_components.component import Component
from ...brains.ability_actors.place_thing_actor import PlaceThingActor
from ....content.farmsteads.defensive_walls import make_fence


@dataclass
class PlaceFenceActor(PlaceThingActor):
    gold_cost: int = 5

    def make_thing(self, x: int, y: int) -> Tuple[int, List[Component]]:
        return make_fence(x, y)
