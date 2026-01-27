"""System for resolving WrathEffect components."""

from __future__ import annotations

from engine import GameScene
from engine.logging import get_logger
from horderl.components.actors.hordeling_spawner import HordelingSpawner
from horderl.components.events.die_events import Die
from horderl.components.tags.tag import Tag, TagType
from horderl.components.wrath_effect import WrathEffect
from horderl.systems.utilities import is_energy_ready


def _trigger_wrath(scene: GameScene, effect: WrathEffect) -> None:
    # Wrath is a one-shot purge that destroys spawners and hordelings.
    logger = get_logger(__name__)
    effect._log_debug("wrath triggered")
    logger.debug("Erasing the origin of evil")
    spawners = scene.cm.get(HordelingSpawner)
    for spawner in spawners:
        scene.cm.delete(spawner.entity)

    effect._log_info("Obliterating hordelings")
    hordelings = [
        tag.entity
        for tag in scene.cm.get(
            Tag, query=lambda tag: tag.tag_type == TagType.HORDELING
        )
    ]
    for hordeling in hordelings:
        scene.cm.add(Die(entity=hordeling, killer=scene.player))
    scene.cm.delete_component(effect)


def run(scene: GameScene) -> None:
    """
    Resolve any active WrathEffect components in the scene.

    Args:
        scene: Scene providing the component manager and player reference.

    Side Effects:
        - Deletes hordeling spawner entities.
        - Emits Die events for all hordelings.
        - Removes WrathEffect components after firing.

    """
    for effect in list(scene.cm.get(WrathEffect)):
        if not is_energy_ready(effect):
            continue
        _trigger_wrath(scene, effect)
