from dataclasses import dataclass

from engine import core
from horderl.components.world_building.world_parameters import WorldParameters


def mark_world_build_complete(scene):
    """Mark the world as built in the WorldParameters component."""
    logger = core.get_logger(__name__)
    logger.info(f"marking world build complete")
    params = scene.cm.get(WorldParameters)
    if not params:
        # something is definitely wrong, we cannot find the world parameters
        raise ValueError(
            "No WorldParameters component found to mark build complete"
        )
    params = params[0]
    params.worldbuilding_done = True
    logger.info(f"world build marked complete")
