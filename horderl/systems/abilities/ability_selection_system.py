"""System for selecting and cycling through abilities."""

from __future__ import annotations

from typing import List

from horderl.components.abilities.ability import Ability
from horderl.components.abilities.null_ability import NullAbility
from horderl.components.ability_tracker import AbilityTracker


def get_current_ability(scene, tracker: AbilityTracker) -> Ability:
    """
    Return the currently selected ability for a tracker.

    Args:
        scene: Active scene containing a component manager.
        tracker: Tracker component storing the selected ability index.

    Returns:
        The active Ability component or a NullAbility placeholder.

    Side Effects:
        - None.
    """
    abilities = _get_abilities(scene, tracker)
    if not abilities:
        return NullAbility()

    index = tracker.current_ability % len(abilities)
    return abilities[index]


def increment(scene, tracker: AbilityTracker) -> None:
    """
    Advance the selected ability index for a tracker.

    Args:
        scene: Active scene containing a component manager.
        tracker: Tracker component storing the selected ability index.

    Side Effects:
        - Updates tracker.current_ability.
        - Logs the newly selected ability title.
    """
    abilities = _get_abilities(scene, tracker)
    if not abilities:
        tracker._log_debug("increment ignored: no abilities")
        return

    tracker.current_ability = (tracker.current_ability + 1) % len(abilities)
    ability = abilities[tracker.current_ability]
    tracker._log_debug(
        f"increment {tracker.current_ability} - {ability.ability_title}"
    )


def decrement(scene, tracker: AbilityTracker) -> None:
    """
    Decrement the selected ability index for a tracker.

    Args:
        scene: Active scene containing a component manager.
        tracker: Tracker component storing the selected ability index.

    Side Effects:
        - Updates tracker.current_ability.
        - Logs the newly selected ability title.
    """
    abilities = _get_abilities(scene, tracker)
    if not abilities:
        tracker._log_debug("decrement ignored: no abilities")
        return

    tracker.current_ability = (tracker.current_ability - 1) % len(abilities)
    ability = abilities[tracker.current_ability]
    tracker._log_debug(
        f"decrement {tracker.current_ability} - {ability.ability_title}"
    )


# The component manager returns ability components in insertion order.


def _get_abilities(scene, tracker: AbilityTracker) -> List[Ability]:
    return scene.cm.get_all(Ability, entity=tracker.entity)
