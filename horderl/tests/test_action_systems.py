import pytest

from engine.component_manager import ComponentManager
from engine.components import Coordinates
from engine.components.entity import Entity
from horderl.components import Attributes
from horderl.components.actions.attack_action import AttackAction
from horderl.components.actions.eat_action import EatAction
from horderl.components.actions.tunnel_to_point import TunnelToPoint
from horderl.components.events.attack_events import AttackFinished
from horderl.components.stomach import Stomach
from horderl.components.tags.peasant_tag import PeasantTag
from horderl.systems.attack_action_system import run as run_attack_actions
from horderl.systems.eat_action_system import run as run_eat_actions
from horderl.systems.tunnel_to_point_system import run as run_tunnel_actions


class DummyScene:
    def __init__(self):
        self.cm = ComponentManager()
        self.warnings = []

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def test_attack_action_system_applies_damage_and_emits_event():
    scene = DummyScene()
    attacker_id = 1
    target_id = 2
    scene.cm.add(
        Entity(entity=attacker_id, name="attacker"),
        Entity(entity=target_id, name="target"),
        Attributes(entity=target_id, hp=5, max_hp=5),
        AttackAction(entity=attacker_id, target=target_id, damage=2),
    )

    run_attack_actions(scene)

    target_attributes = scene.cm.get_one(Attributes, entity=target_id)
    assert target_attributes.hp == 3
    assert scene.cm.get(AttackAction) == []
    assert len(scene.cm.get(AttackFinished)) == 1
    assert scene.warnings


def test_eat_action_system_stashes_peasant_and_sets_stomach():
    scene = DummyScene()
    eater_id = 10
    target_id = 20
    stomach = Stomach(entity=eater_id)
    scene.cm.add(
        Entity(entity=eater_id, name="eater"),
        Entity(entity=target_id, name="peasant"),
        PeasantTag(entity=target_id),
        stomach,
        EatAction(entity=eater_id, target=target_id),
    )

    run_eat_actions(scene)

    assert target_id in scene.cm.stashed_entities
    assert stomach.contents == target_id
    assert scene.cm.get(EatAction) == []


def test_tunnel_to_point_system_moves_and_spawns_hole():
    scene = DummyScene()
    digger_id = 30
    scene.cm.add(
        Entity(entity=digger_id, name="digger"),
        Coordinates(entity=digger_id, x=1, y=1),
        TunnelToPoint(entity=digger_id, point=(3, 4)),
    )

    run_tunnel_actions(scene)

    coords = scene.cm.get_one(Coordinates, entity=digger_id)
    assert (coords.x, coords.y) == (3, 4)
    assert scene.cm.get(TunnelToPoint) == []
    hole_entities = scene.cm.get(
        Entity, query=lambda ent: ent.name == "hole"
    )
    assert hole_entities
