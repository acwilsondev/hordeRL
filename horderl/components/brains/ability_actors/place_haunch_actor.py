from dataclasses import dataclass

from horderl.components.brains.ability_actors.place_thing_actor import PlaceThingActor
from horderl.content.haunch import make_haunch
from horderl.engine.types import Entity


@dataclass
class PlaceHaunchActor(PlaceThingActor):
    gold_cost: int = 5

    def make_thing(self, x: int, y: int) -> Entity:
        return make_haunch(x, y)
