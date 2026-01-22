from dataclasses import dataclass

from horderl.components.brains.ability_actors.place_thing_actor import (
    PlaceThingActor,
)


@dataclass
class PlaceCowActor(PlaceThingActor):
    """Command component for placing cow entities."""

    gold_cost: int = 100
    spawn_key: str = "cow"
