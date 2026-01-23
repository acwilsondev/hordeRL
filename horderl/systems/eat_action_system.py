from engine.components.entity import Entity
from horderl.components.actions.eat_action import EatAction
from horderl.components.events.die_events import Die
from horderl.components.stomach import Stomach
from horderl.components.tags.tag import Tag, TagType


def run(scene) -> None:
    """
    Resolve queued eat actions.

    Args:
        scene: Active game scene.

    Side effects:
        - Removes or stashes eaten entities.
        - Updates stomach contents.
        - Deletes EatAction components.
    """
    for action in scene.cm.get(EatAction):
        if action.can_act():
            execute(scene, action)


def execute(scene, action: EatAction) -> None:
    """
    Execute a single eat action.

    Args:
        scene: Active game scene.
        action: The eat action data component.
    """
    action._log_debug(f"attempting to eat {action.target}")
    this_entity = scene.cm.get_one(Entity, entity=action.entity)
    target_entity = scene.cm.get_one(Entity, entity=action.target)
    if not target_entity:
        action._log_debug(f"attempted to eat {action.target} but it was gone!")
        return
    scene.warn(f"{this_entity.name} ate a {target_entity.name}!")
    if any(
        tag.tag_type == TagType.PEASANT
        for tag in scene.cm.get_all(Tag, entity=action.target)
    ):
        scene.cm.stash_entity(action.target)
        stomach = scene.cm.get_one(Stomach, entity=action.entity)
        stomach.contents = action.target
    else:
        scene.cm.add(Die(entity=action.target, killer=action.entity))

    scene.cm.delete_component(action)
