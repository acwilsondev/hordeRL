from dataclasses import dataclass

from engine.component_manager import ComponentManager
from horderl.components.animation_definitions.blinker_animation_definition import (
    BlinkerAnimationDefinition,
)
from horderl.components.brains.brain import Brain
from horderl.systems import brain_stack


class DummyScene:
    """Provide the minimal scene surface needed for brain stack tests."""

    def __init__(self) -> None:
        self.cm = ComponentManager()
        self.hook_called = False


@dataclass
class HookBrain(Brain):
    """Brain with a back-out hook to verify cleanup behavior."""

    def _on_back_out(self, scene) -> None:
        scene.hook_called = True


def test_swap_stashes_old_brain_and_sets_stack_metadata() -> None:
    scene = DummyScene()
    entity = 10
    old_brain = Brain(entity=entity)
    new_brain = Brain(entity=entity)
    scene.cm.add(old_brain)

    brain_stack.swap(scene, entity, new_brain)

    assert old_brain.id in scene.cm.stashed_components
    assert scene.cm.get_one(Brain, entity=entity) is new_brain
    assert new_brain.old_brain == old_brain.id


def test_back_out_restores_brain_and_cleans_blinker() -> None:
    scene = DummyScene()
    entity = 42
    old_brain = Brain(entity=entity)
    scene.cm.add(old_brain)
    scene.cm.stash_component(old_brain.id)

    new_brain = HookBrain(entity=entity, old_brain=old_brain.id)
    blinker = BlinkerAnimationDefinition(entity=entity)
    scene.cm.add(new_brain, blinker)

    restored = brain_stack.back_out(scene, new_brain)

    assert restored is old_brain
    assert scene.cm.get_one(Brain, entity=entity) is old_brain
    assert new_brain not in scene.cm.get(Brain)
    assert blinker.is_animating is False
    assert blinker.remove_on_stop is True
    assert scene.hook_called is True
