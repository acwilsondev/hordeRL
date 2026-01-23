from dataclasses import dataclass

from horderl.components.brains.ability_actors.place_thing_actor import (
    PlaceThingActor,
)


@dataclass
class PlaceStoneWallActor(PlaceThingActor):
    """Command component for placing stone wall entities."""

    gold_cost: int = 10
    spawn_key: str = "stone_wall"
