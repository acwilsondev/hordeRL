from dataclasses import dataclass

from horderl.components.brains.ability_actors.place_thing_actor import (
    PlaceThingActor,
)
from horderl.content.bomb import make_bomb
from horderl.engine.types import Entity


@dataclass
class PlaceBombActor(PlaceThingActor):
    gold_cost: int = 10

    def make_thing(self, x: int, y: int) -> Entity:
        return make_bomb(x, y)
