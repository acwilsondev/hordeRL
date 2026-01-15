from types import SimpleNamespace

from engine.component_manager import ComponentManager
from engine.components import Actor, Coordinates
from engine.components.entity import Entity
from horderl import palettes
from horderl.components import Appearance
from horderl.components.animation_definitions import (
    BlinkerAnimationDefinition,
    FloatAnimationDefinition,
    PathAnimationDefinition,
    RandomizedBlinkerAnimationDefinition,
    ResetOwnerAnimationDefinition,
    SequenceAnimationDefinition,
)
from horderl.components.events.delete_event import Delete
from horderl.components.path_node import PathNode
from horderl.components.relationships.owner import Owner
from horderl.systems.animation_controller_system import run as run_animations


class DummyScene:
    def __init__(self):
        self.cm = ComponentManager()
        self.config = SimpleNamespace(map_width=20, map_height=20)


def test_blinker_animation_toggles_and_restores():
    scene = DummyScene()
    entity_id = 1
    appearance = Appearance(
        entity=entity_id,
        symbol="a",
        color=palettes.WHITE,
        bg_color=palettes.BACKGROUND,
    )
    animation = BlinkerAnimationDefinition(
        entity=entity_id,
        timer_delay=0,
        new_symbol="b",
        new_color=palettes.DEBUG,
        new_bg_color=palettes.BACKGROUND,
    )
    scene.cm.add(Entity(entity=entity_id, name="blink"), appearance, animation)

    run_animations(scene, 0)
    assert appearance.symbol == "a"

    run_animations(scene, 0)
    assert appearance.symbol == "b"

    animation.is_animating = False
    run_animations(scene, 0)
    assert appearance.symbol == "a"


def test_randomized_blinker_updates_timer_delay():
    scene = DummyScene()
    entity_id = 2
    appearance = Appearance(
        entity=entity_id,
        symbol="~",
        color=palettes.WATER,
        bg_color=palettes.BACKGROUND,
    )
    animation = RandomizedBlinkerAnimationDefinition(
        entity=entity_id,
        timer_delay=0,
        min_timer_delay=5,
        max_timer_delay=5,
        new_symbol="~",
        new_color=palettes.DEBUG,
        new_bg_color=palettes.BACKGROUND,
    )
    scene.cm.add(Entity(entity=entity_id, name="water"), appearance, animation)

    run_animations(scene, 0)

    assert animation.timer_delay == 5


def test_float_animation_deletes_entity_on_completion():
    scene = DummyScene()
    entity_id = 3
    scene.cm.add(
        Entity(entity=entity_id, name="floaty"),
        Coordinates(entity=entity_id, x=1, y=10),
        FloatAnimationDefinition(entity=entity_id, timer_delay=0, duration=0),
    )

    run_animations(scene, 0)

    assert entity_id not in scene.cm.entities


def test_path_animation_steps_through_nodes():
    scene = DummyScene()
    entity_id = 4
    scene.cm.add(
        Entity(entity=entity_id, name="path"),
        Coordinates(entity=entity_id, x=0, y=0),
        PathAnimationDefinition(entity=entity_id, timer_delay=0),
        PathNode(entity=entity_id, step=0, x=3, y=4),
    )

    run_animations(scene, 0)

    coords = scene.cm.get_one(Coordinates, entity=entity_id)
    assert (coords.x, coords.y) == (3, 4)


def test_sequence_animation_sets_appearance():
    scene = DummyScene()
    entity_id = 5
    appearance = Appearance(
        entity=entity_id,
        symbol=".",
        color=palettes.WHITE,
        bg_color=palettes.BACKGROUND,
    )
    animation = SequenceAnimationDefinition(
        entity=entity_id,
        timer_delay=0,
        sequence=[(palettes.GOLD, "*")],
    )
    scene.cm.add(Entity(entity=entity_id, name="explosion"), appearance, animation)

    run_animations(scene, 0)

    assert appearance.symbol == "*"
    assert appearance.color == palettes.GOLD


def test_reset_owner_animation_sets_can_animate():
    scene = DummyScene()
    owner_id = 10
    entity_id = 11
    peasant = Actor(entity=owner_id)
    peasant.can_animate = False
    scene.cm.add(
        Entity(entity=owner_id, name="peasant"),
        peasant,
        Entity(entity=entity_id, name="farm_animation"),
        Owner(entity=entity_id, owner=owner_id),
        ResetOwnerAnimationDefinition(entity=entity_id),
        Delete(entity=entity_id, next_update=0),
    )

    run_animations(scene, 0)

    assert peasant.can_animate is True
