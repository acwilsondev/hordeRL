from typing import List

from engine.components import Coordinates
from engine.components.entity import Entity
from horderl.components import Attributes
from horderl.components.actions.attack_action import AttackAction
from horderl.components.attacks.attack_effects.attack_effect import (
    AttackEffect,
)
from horderl.components.cry_for_help import CryForHelp
from horderl.components.events.attack_events import AttackFinished
from horderl.components.events.die_events import Die
from horderl.components.house_structure import HouseStructure
from horderl.components.relationships.owner import Owner
from horderl.content.states import help_animation
from horderl.i18n import t


def run(scene) -> None:
    """
    Process all attack actions currently queued in the component manager.

    Args:
        scene: Active game scene.

    Side effects:
        - Applies damage or effects to targets.
        - Emits AttackFinished events.
        - Removes AttackAction components after execution.
    """
    for action in scene.cm.get(AttackAction):
        if action.can_act():
            execute(scene, action)


def execute(scene, action: AttackAction) -> None:
    """
    Resolve a single attack action.

    Args:
        scene: Active game scene.
        action: The attack action data component.

    Side effects:
        - Modifies entity health.
        - Adds events and animations.
        - Deletes AttackAction components.
    """
    this_entity = scene.cm.get_one(Entity, entity=action.entity)
    target_entity = scene.cm.get_one(Entity, entity=action.target)

    scene.warn(
        t(
            "message.attack_damage",
            attacker=this_entity.name,
            damage=action.damage,
            target=target_entity.name,
        )
    )

    action._log_info(f"dealing {action.damage} dmg to {action.target}")
    owner = scene.cm.get_one(Owner, entity=action.target)
    if owner:
        structures = scene.cm.get(
            HouseStructure, query=lambda hs: hs.house_id == owner.owner
        )
        house_structure = structures[0] if structures else None
    else:
        house_structure = None

    if house_structure:
        _handle_house_damage(scene, action, house_structure, action.damage)
    else:
        attack_effects: List[AttackEffect] = scene.cm.get_all(
            AttackEffect, entity=action.entity
        )
        for attack_effect in attack_effects:
            attack_effect.apply(scene, action.entity, action.target)
        _handle_entity_damage(scene, action, action.target, action.damage)

    cry_for_help = scene.cm.get_one(CryForHelp, entity=action.target)
    if cry_for_help:
        coords = scene.cm.get_one(Coordinates, entity=action.target)
        help_anim = help_animation(coords.x, coords.y)
        scene.cm.add(*help_anim[1])

    scene.cm.delete_components(AttackAction)
    scene.cm.add(AttackFinished(entity=action.entity))


def _handle_house_damage(
    scene, action: AttackAction, house_structure, damage: int
) -> None:
    # Assumes house_structure entities are valid combat targets.
    for entity in house_structure.get_all():
        _handle_entity_damage(scene, action, entity, damage)


def _handle_entity_damage(
    scene, action: AttackAction, target: int, damage: int
) -> None:
    target_attributes = scene.cm.get_one(Attributes, entity=target)
    if target_attributes:
        target_attributes.hp -= damage
        target_attributes.hp = max(0, target_attributes.hp)
        if target_attributes.hp <= 0:
            action._log_info("applying Die effect")
            scene.cm.add(Die(entity=target_attributes.entity, killer=action.entity))
