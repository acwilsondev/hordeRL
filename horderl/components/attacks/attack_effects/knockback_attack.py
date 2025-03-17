from dataclasses import dataclass

from horderl.components import Coordinates
from horderl.components.attacks.attack_effects.attack_effect import AttackEffect
from horderl.content.states import knockback_animation


@dataclass
class KnockbackAttack(AttackEffect):
    def apply(self, scene, source, target):
        self._log_info("knocked back target")
        source_coords = scene.cm.get_one(Coordinates, entity=source)
        target_coords = scene.cm.get_one(Coordinates, entity=target)

        direction = source_coords.direction_towards(target_coords)
        target_coords.x += direction[0]
        target_coords.y += direction[1]

        attack_animation = knockback_animation(target_coords.x, target_coords.y)
        scene.cm.add(*attack_animation[1])
