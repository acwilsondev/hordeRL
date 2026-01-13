from dataclasses import dataclass

from engine.components import Coordinates
from horderl.components.actions.attack_action import AttackAction
from horderl.components.attacks.attack import Attack
from horderl.content.attacks import stab


@dataclass
class StandardAttack(Attack):
    damage: int = 1

    def apply_attack(self, scene, target):
        self._log_debug(f"applying attack against {target}")
        scene.cm.add(AttackAction(entity=self.entity, target=target, damage=1))
        target_coords = scene.cm.get_one(Coordinates, target)
        scene.cm.add(*stab(self.entity, target_coords.x, target_coords.y)[1])
