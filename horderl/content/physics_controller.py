from engine import core

from ..components.flood_nearby_holes import FloodHolesState


def make_physics_controller():
    entity_id = core.get_id()

    return (
        entity_id,
        [
            FloodHolesState(entity=entity_id),
        ],
    )
