"""System for reacting to tree-cut events that affect world beauty."""

from __future__ import annotations

from engine import GameScene, core
from horderl import palettes
from horderl.components.events.tree_cut_event import TreeCutEvent
from horderl.components.world_beauty import WorldBeauty
from horderl.components.world_building.world_parameters import WorldParameters


def _apply_tree_cut(
    scene: GameScene, event: TreeCutEvent, listener: WorldBeauty
) -> None:
    # Tree-cut events increment counters and can anger the spirits.
    listener._log_info("detected tree cut")
    listener.trees_cut += 1
    if listener.trees_cut % listener.spirits_attitude:
        return

    scene.message(
        "The spirits grow angrier with your cutting.",
        color=palettes.BLOOD,
    )
    world_params = scene.cm.get_one(
        WorldParameters, entity=core.get_id("world")
    )
    listener.spirits_wrath += 1
    listener.spirits_attitude = max(
        1, listener.spirits_attitude - world_params.tree_cut_anger
    )
    listener._log_info(
        f"decreased wrath {listener.spirits_wrath} and attitude"
        f" {listener.spirits_attitude}"
    )


def run(scene: GameScene) -> None:
    """
    Process TreeCutEvent components and update WorldBeauty state.

    Args:
        scene: Scene providing the component manager and messaging utilities.

    Side Effects:
        - Updates WorldBeauty counters for tree cuts and spirit anger.
        - Sends spirit warning messages when thresholds are hit.
        - Removes processed TreeCutEvent components from the manager.

    """
    for event in list(scene.cm.get(TreeCutEvent)):
        for listener in scene.cm.get(WorldBeauty):
            _apply_tree_cut(scene, event, listener)
        scene.cm.delete_component(event)
