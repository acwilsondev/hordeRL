from dataclasses import dataclass

from .. import Coordinates
from ..actions.attack_action import AttackAction
from ..attacks.attack import Attack
from ..structure import Structure
from ...content.attacks import stab


@dataclass
class SiegeAttack(Attack):
    """Deals heavy damage to structures."""

    damage: int = 1

    def apply_attack(self, scene, target):
        self._log_debug(f"applying attack against {target}")
        structure = scene.cm.get_one(Structure, entity=target)
        damage = self.damage * 5 if structure else self.damage
        scene.cm.add(AttackAction(entity=self.entity, target=target, damage=damage))
        target_coords = scene.cm.get_one(Coordinates, target)
        scene.cm.add(*stab(self.entity, target_coords.x, target_coords.y)[1])
