from dataclasses import dataclass
from typing import List, Tuple

from components.base_components.component import Component
from components.brains.ability_actors.place_thing_actor import PlaceThingActor
from content.farmsteads.defensive_walls import make_fence
from content.spike_trap import make_spike_trap


@dataclass
class PlaceSpikesActor(PlaceThingActor):
    gold_cost: int = 5

    def make_thing(self, x: int, y: int) -> Tuple[int, List[Component]]:
        return make_spike_trap(x, y)
