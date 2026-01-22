"""System for applying population changes from peasant events."""

from __future__ import annotations

from engine import GameScene
from horderl.components.events.peasant_events import PeasantAdded, PeasantDied
from horderl.components.population import Population
from horderl.i18n import t


def _apply_peasant_added(
    scene: GameScene, event: PeasantAdded, listener: Population
) -> None:
    # Events do not target specific population trackers.
    listener._log_info("population increased")
    listener.population += 1


def _apply_peasant_died(
    scene: GameScene, event: PeasantDied, listener: Population
) -> None:
    # A population collapse ends the scene.
    listener._log_info("population decreased")
    listener.population -= 1
    if listener.population <= 0:
        scene.popup_message(t("message.peasants_dead"))
        scene.pop()


def run(scene: GameScene) -> None:
    """
    Apply population adjustments triggered by peasant event components.

    Args:
        scene: Scene providing the component manager and UI messaging helpers.

    Side Effects:
        - Updates Population component counts when peasants are added or die.
        - Emits popup messaging and pops the scene on total population loss.
        - Removes processed peasant event components from the manager.

    """
    for event in list(scene.cm.get(PeasantAdded)):
        for listener in scene.cm.get(Population):
            _apply_peasant_added(scene, event, listener)
        scene.cm.delete_component(event)

    for event in list(scene.cm.get(PeasantDied)):
        for listener in scene.cm.get(Population):
            _apply_peasant_died(scene, event, listener)
        scene.cm.delete_component(event)
