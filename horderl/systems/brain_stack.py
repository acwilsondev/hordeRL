from engine import GameScene
from horderl.components.animation_definitions.blinker_animation_definition import (
    BlinkerAnimationDefinition,
)
from horderl.components.brains.brain import Brain


def swap(scene: GameScene, entity: int, new_brain: Brain) -> None:
    """
    Swap the active brain for an entity, stashing the previous brain.

    Args:
        scene: The active game scene.
        entity: The entity whose brain should be swapped.
        new_brain: The new brain component to activate.

    Side effects:
        - Stashes the existing brain component.
        - Adds the new brain component to the scene.

    Raises:
        ValueError: If no active brain exists for the entity.
    """
    current_brain = scene.cm.get_one(Brain, entity=entity)
    if not current_brain:
        raise ValueError(f"No active brain found for entity {entity}")

    new_brain.old_brain = current_brain.id
    scene.cm.stash_component(current_brain.id)
    scene.cm.add(new_brain)


def back_out(scene: GameScene, brain: Brain) -> Brain:
    """
    Restore the previous brain and remove the current brain component.

    Args:
        scene: The active game scene.
        brain: The current brain component to back out from.

    Returns:
        The previously stashed brain component.

    Side effects:
        - Calls any brain-specific back-out hook.
        - Unstashes the previous brain component.
        - Stops any blinker animation on the brain's entity.
        - Removes the current brain component from the scene.
    """
    _run_back_out_hook(scene, brain)
    old_actor = scene.cm.unstash_component(brain.old_brain)
    _cleanup_blinker(scene, brain.entity)
    scene.cm.delete_component(brain)
    return old_actor


def _run_back_out_hook(scene: GameScene, brain: Brain) -> None:
    # Some brain subclasses define a private hook for back-out cleanup.
    hook = getattr(brain, "_on_back_out", None)
    if callable(hook):
        hook(scene)


def _cleanup_blinker(scene: GameScene, entity: int) -> None:
    # Ensure lingering blinker animations get cleaned up during back-out.
    blinker = scene.cm.get_one(BlinkerAnimationDefinition, entity=entity)
    if blinker:
        blinker.is_animating = False
        blinker.remove_on_stop = True
