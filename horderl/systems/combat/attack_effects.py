from __future__ import annotations

from typing import Callable, Dict

from engine.components import Coordinates
from horderl.components.attacks.attack_effects.attack_effect_resolution import (
    AttackEffectResolution,
)
from horderl.content.states import knockback_animation

EffectHandler = Callable[[object, AttackEffectResolution], None]
KNOCKBACK_DISTANCE_KEY = "distance"


def run(scene) -> None:
    """
    Resolve queued attack effects into world state changes.

    Args:
        scene: Active game scene with a component manager.

    Components Consumed:
        - AttackEffectResolution for pending effect execution.

    Side Effects:
        - Updates entity positions for forced movement effects.
        - Adds combat animation components.
        - Deletes processed effect resolution components.
    """
    handlers: Dict[str, EffectHandler] = {
        "knockback": _apply_knockback,
    }

    for effect in list(scene.cm.get(AttackEffectResolution)):
        handler = handlers.get(effect.effect_type)
        if handler:
            handler(scene, effect)
        else:
            effect._log_warning(
                f"unknown attack effect type '{effect.effect_type}'"
            )
        scene.cm.delete_component(effect)


def _apply_knockback(scene, effect: AttackEffectResolution) -> None:
    # Assumes coordinates exist for both source and target entities.
    source_coords = scene.cm.get_one(Coordinates, entity=effect.source)
    target_coords = scene.cm.get_one(Coordinates, entity=effect.target)
    if not source_coords or not target_coords:
        effect._log_warning("missing coordinates for knockback resolution")
        return

    distance = int(effect.parameters.get(KNOCKBACK_DISTANCE_KEY, 1))
    direction = source_coords.direction_towards(target_coords)
    target_coords.x += direction[0] * distance
    target_coords.y += direction[1] * distance

    attack_animation = knockback_animation(target_coords.x, target_coords.y)
    scene.cm.add(*attack_animation[1])
