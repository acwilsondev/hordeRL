from dataclasses import dataclass

from ...base_components.component import Component
from ..ability_actors.place_thing_actor import PlaceThingActor
from ....content.farmsteads.defensive_walls import make_stone_wall


@dataclass
class PlaceStoneWallActor(PlaceThingActor):
    gold_cost: int = 10

    def make_thing(self, x: int, y: int) -> tuple[int, list[Component]]:
        return make_stone_wall(x, y)
