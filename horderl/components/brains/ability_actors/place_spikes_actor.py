from dataclasses import dataclass

from horderl.components.brains.ability_actors.place_thing_actor import (
    PlaceThingActor,
)


@dataclass
class PlaceSpikesActor(PlaceThingActor):
    """Command component for placing spike trap entities."""

    gold_cost: int = 5
    spawn_key: str = "spike_trap"
