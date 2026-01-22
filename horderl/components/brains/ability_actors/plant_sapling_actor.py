from dataclasses import dataclass

from horderl.components.brains.ability_actors.place_thing_actor import (
    PlaceThingActor,
)


@dataclass
class PlaceSaplingActor(PlaceThingActor):
    """Command component for placing sapling entities."""

    gold_cost: int = 1
    spawn_key: str = "sapling"
