from dataclasses import dataclass

from horderl.components.brains.ability_actors.place_thing_actor import (
    PlaceThingActor,
)


@dataclass
class PlaceBombActor(PlaceThingActor):
    """Command component for placing bomb entities."""

    gold_cost: int = 10
    spawn_key: str = "bomb"
