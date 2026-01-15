from engine import core

from ..components.flood_nearby_holes import FloodHolesController


def make_physics_controller():
    entity_id = core.get_id()

    return (
        entity_id,
        [
            FloodHolesController(entity=entity_id),
        ],
    )
