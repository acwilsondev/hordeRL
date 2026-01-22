"""System for converting attack-finished events into death events."""

from __future__ import annotations

from engine import GameScene
from horderl.components.die_on_attack_finished import DieOnAttackFinished
from horderl.components.events.attack_events import AttackFinished
from horderl.components.events.die_events import Die


def _apply_attack_finished(
    scene: GameScene,
    event: AttackFinished,
    listener: DieOnAttackFinished,
) -> None:
    # Only apply when the finished attack belongs to the listener.
    if event.entity == listener.entity:
        scene.cm.add(Die(entity=listener.entity))


def run(scene: GameScene) -> None:
    """
    Convert AttackFinished events into Die events for marked entities.

    Args:
        scene: Scene providing the component manager.

    Side Effects:
        - Adds Die events when matching DieOnAttackFinished components exist.
        - Removes processed AttackFinished event components from the manager.

    """
    for event in list(scene.cm.get(AttackFinished)):
        for listener in scene.cm.get(DieOnAttackFinished):
            _apply_attack_finished(scene, event, listener)
        scene.cm.delete_component(event)
