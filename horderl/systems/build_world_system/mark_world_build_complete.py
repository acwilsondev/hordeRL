from dataclasses import dataclass

from engine import core
from horderl.components.system_control_options import SystemControlOptions


def mark_world_build_complete(scene):
    """Mark the world as built in the WorldParameters component."""
    logger = core.get_logger(__name__)
    logger.info(f"marking world build complete")
    options = scene.cm.get_one(SystemControlOptions, entity=core.get_id("world"))
    options.worldbuilding_done = True
    logger.info(f"world build marked complete")
