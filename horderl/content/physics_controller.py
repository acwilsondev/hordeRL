from engine import core

from ..components.flood_nearby_holes import FloodHolesSystem


def make_physics_controller():
    entity_id = core.get_id()

    return (
        entity_id,
        [
            FloodHolesSystem(entity=entity_id),
        ],
    )
