from dataclasses import dataclass

from .place_thing_actor import PlaceThingActor
from ....content.cows import make_cow
from ....engine.types import Entity


@dataclass
class PlaceCowActor(PlaceThingActor):
    gold_cost: int = 100

    def make_thing(self, x: int, y: int) -> Entity:
        return make_cow(x, y)
