from dataclasses import dataclass

from horderl.components.brains.ability_actors.place_thing_actor import PlaceThingActor
from horderl.content.cows import make_cow
from horderl.engine.types import Entity


@dataclass
class PlaceCowActor(PlaceThingActor):
    gold_cost: int = 100

    def make_thing(self, x: int, y: int) -> Entity:
        return make_cow(x, y)
