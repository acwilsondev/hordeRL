from dataclasses import dataclass

from horderl.components.brains.ability_actors.place_thing_actor import (
    PlaceThingActor,
)


@dataclass
class HireKnightActor(PlaceThingActor):
    """Command component for hiring knight entities."""

    gold_cost: int = 100
    spawn_key: str = "knight"
