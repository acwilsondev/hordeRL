from dataclasses import dataclass

from horderl.components.brains.ability_actors.place_thing_actor import (
    PlaceThingActor,
)


@dataclass
class PlaceFenceActor(PlaceThingActor):
    """Command component for placing fence entities."""

    gold_cost: int = 5
    spawn_key: str = "fence"
