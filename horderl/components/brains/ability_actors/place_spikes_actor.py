from dataclasses import dataclass
from typing import List, Tuple

from ...base_components.component import Component
from .place_thing_actor import PlaceThingActor
from ....content.spike_trap import make_spike_trap


@dataclass
class PlaceSpikesActor(PlaceThingActor):
    gold_cost: int = 5

    def make_thing(self, x: int, y: int) -> Tuple[int, List[Component]]:
        return make_spike_trap(x, y)
