from dataclasses import dataclass

from engine.components.component import Component
from horderl.components.brains.ability_actors.place_thing_actor import (
    PlaceThingActor,
)
from horderl.content.farmsteads.defensive_walls import make_stone_wall


@dataclass
class PlaceStoneWallActor(PlaceThingActor):
    gold_cost: int = 10

    def make_thing(self, x: int, y: int) -> tuple[int, list[Component]]:
        return make_stone_wall(x, y)
