from dataclasses import dataclass
from typing import List

from horderl.components import Attributes, Coordinates
from horderl.components.attacks.attack_effects.attack_effect import (
    AttackEffect,
)
from horderl.components.cry_for_help import CryForHelp
from horderl.components.events.attack_events import AttackFinished
from horderl.components.events.die_events import Die
from horderl.components.house_structure import HouseStructure
from horderl.components.relationships.owner import Owner
from horderl.content.states import help_animation
from horderl.engine import constants
from horderl.engine.components.energy_actor import EnergyActor
from horderl.engine.components.entity import Entity


@dataclass
class AttackAction(EnergyActor):
    """
    Instance of a live attack.
    """

    target: int = constants.INVALID
    damage: int = 0

    def act(self, scene) -> None:
        this_entity = scene.cm.get_one(Entity, entity=self.entity)
        target_entity = scene.cm.get_one(Entity, entity=self.target)

        scene.warn(
            f"{this_entity.name} dealt {self.damage} dmg to"
            f" {target_entity.name}!"
        )

        self._log_info(f"dealing {self.damage} dmg to {self.target}")
        owner = scene.cm.get_one(Owner, entity=self.target)
        if owner:
            structures = scene.cm.get(
                HouseStructure, query=lambda hs: hs.house_id == owner.owner
            )
            house_structure = structures[0] if structures else None
        else:
            house_structure = None

        if house_structure:
            self._handle_house_damage(scene, house_structure, self.damage)
        else:
            attack_effects: List[AttackEffect] = scene.cm.get_all(
                AttackEffect, entity=self.entity
            )
            for attack_effect in attack_effects:
                attack_effect.apply(scene, self.entity, self.target)
            self._handle_entity_damage(scene, self.target, self.damage)

        cry_for_help = scene.cm.get_one(CryForHelp, entity=self.target)
        if cry_for_help:
            coords = scene.cm.get_one(Coordinates, entity=self.target)
            help_anim = help_animation(coords.x, coords.y)
            scene.cm.add(*help_anim[1])

        scene.cm.delete_components(AttackAction)
        scene.cm.add(AttackFinished(entity=self.entity))

    def _handle_house_damage(self, scene, house_structure, damage):
        for entity in house_structure.get_all():
            self._handle_entity_damage(scene, entity, damage)

    def _handle_entity_damage(self, scene, target, damage):
        target_attributes = scene.cm.get_one(Attributes, entity=target)
        if target_attributes:
            target_attributes.hp -= damage
            target_attributes.hp = max(0, target_attributes.hp)
            if target_attributes.hp <= 0:
                self._log_info(f"applying Die effect")
                scene.cm.add(
                    Die(entity=target_attributes.entity, killer=self.entity)
                )
