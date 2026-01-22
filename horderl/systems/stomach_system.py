"""System helpers for stomach component side effects."""

from __future__ import annotations

from engine import GameScene, constants
from horderl.components.stomach import Stomach


def clear_stomach(scene: GameScene, stomach: Stomach) -> None:
    """
    Drop the stashed entity referenced by the stomach and clear its contents.

    Args:
        scene: Scene providing the component manager and stash operations.
        stomach: Stomach component whose contents should be dropped.

    Side Effects:
        - Drops the stashed entity from the component manager.
        - Updates the stomach contents to INVALID.

    """
    if stomach.contents == constants.INVALID:
        return

    stomach._log_debug(f"clearing contents {stomach.contents}")
    scene.cm.drop_stashed_entity(stomach.contents)
    stomach.contents = constants.INVALID


def dump_stomach(scene: GameScene, stomach: Stomach) -> None:
    """
    Unstash the entity stored in the stomach, typically after the owner dies.

    Args:
        scene: Scene providing the component manager and stash operations.
        stomach: Stomach component whose contents should be released.

    Side Effects:
        - Unstashes the stored entity.
        - Updates the stomach contents to INVALID.

    """
    if stomach.contents == constants.INVALID:
        stomach._log_debug("nothing to dump")
        return

    stomach._log_debug(f"dumping {stomach.contents}")
    scene.cm.unstash_entity(stomach.contents)
    stomach.contents = constants.INVALID
