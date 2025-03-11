import logging
from dataclasses import dataclass

from components import Coordinates
from components.actions.attack_action import AttackAction
from components.attacks.attack import Attack
from content.attacks import stab


@dataclass
class StandardAttack(Attack):
    damage: int = 1

    def apply_attack(self, scene, target):
        self._log_debug(f"applying attack against {target}")
        scene.cm.add(AttackAction(entity=self.entity, target=target, damage=1))
        target_coords = scene.cm.get_one(Coordinates, target)
        scene.cm.add(*stab(self.entity, target_coords.x, target_coords.y)[1])
