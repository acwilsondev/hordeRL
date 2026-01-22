from engine.component_manager import ComponentManager
from engine.components import Coordinates
from engine.components.entity import Entity
from horderl.components.attacks.attack_effects.attack_effect_resolution import (
    AttackEffectResolution,
)
from horderl.systems.combat.attack_effects import run as run_attack_effects


class DummyScene:
    """Minimal scene stub for combat system tests."""

    def __init__(self):
        self.cm = ComponentManager()


def test_attack_effects_system_applies_knockback():
    scene = DummyScene()
    source_id = 1
    target_id = 2
    scene.cm.add(
        Coordinates(entity=source_id, x=1, y=1),
        Coordinates(entity=target_id, x=2, y=1),
        AttackEffectResolution(
            entity=source_id,
            source=source_id,
            target=target_id,
            effect_type="knockback",
            parameters={"distance": 2},
        ),
    )

    run_attack_effects(scene)

    target_coords = scene.cm.get_one(Coordinates, entity=target_id)
    assert (target_coords.x, target_coords.y) == (4, 1)
    assert scene.cm.get(AttackEffectResolution) == []
    assert scene.cm.get(
        Entity, query=lambda ent: ent.name == "knockback_animation"
    )
