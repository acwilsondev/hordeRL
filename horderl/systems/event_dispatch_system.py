"""System for dispatching event components to their listeners."""

from dataclasses import dataclass
from typing import Callable, Dict, Optional, Type

from engine import GameScene
from engine.components import Coordinates
from engine.components.component import Component
from horderl.components.events.attack_events import (
    AttackFinished,
    OnAttackFinishedListener,
)
from horderl.components.events.dally_event import DallyEvent
from horderl.components.events.delete_event import Delete, DeleteListener
from horderl.components.events.die_events import Die
from horderl.components.events.new_day_event import DayBegan, DayBeganListener
from horderl.components.events.peasant_events import (
    PeasantAdded,
    PeasantAddedListener,
    PeasantDied,
    PeasantDiedListener,
)
from horderl.components.events.quit_game_events import (
    QuitGame,
    QuitGameListener,
)
from horderl.components.events.start_game_events import (
    GameStartListener,
    StartGame,
)
from horderl.components.events.step_event import (
    EnterEvent,
    EnterListener,
    StepEvent,
)
from horderl.components.events.terrain_changed_event import (
    TerrainChangedEvent,
    TerrainChangedListener,
)
from horderl.components.events.tree_cut_event import (
    TreeCutEvent,
    TreeCutListener,
)
from horderl.components.serialization.save_game import SaveGame
from horderl.scenes.start_menu import get_start_menu
from horderl.systems.serialization_system import save_game


@dataclass(frozen=True)
class EventDispatchRule:
    """Define how to route an event to its listeners and follow-up actions."""

    listener_type: Optional[Type[Component]]
    notify: Optional[Callable[[GameScene, Component, Component], None]]
    after_notify: Optional[Callable[[GameScene, Component], None]] = None
    after_remove: Optional[Callable[[GameScene, Component], None]] = None
    consume: bool = True


def _notify_attack_finished(
    scene: GameScene,
    event: AttackFinished,
    listener: OnAttackFinishedListener,
) -> None:
    listener.on_attack_finished(scene, event.entity)


def _notify_day_began(
    scene: GameScene, event: DayBegan, listener: DayBeganListener
) -> None:
    listener.on_new_day(scene, event.day)


def _notify_delete(
    scene: GameScene, event: Delete, listener: DeleteListener
) -> None:
    if listener.entity == event.entity:
        listener.on_delete(scene)


def _notify_peasant_added(
    scene: GameScene, event: PeasantAdded, listener: PeasantAddedListener
) -> None:
    listener.on_peasant_added(scene)


def _notify_peasant_died(
    scene: GameScene, event: PeasantDied, listener: PeasantDiedListener
) -> None:
    listener.on_peasant_died(scene)


def _notify_quit_game(
    scene: GameScene, event: QuitGame, listener: QuitGameListener
) -> None:
    listener.on_quit_game(scene)


def _notify_start_game(
    scene: GameScene, event: StartGame, listener: GameStartListener
) -> None:
    listener.on_game_start(scene)


def _notify_terrain_changed(
    scene: GameScene,
    event: TerrainChangedEvent,
    listener: TerrainChangedListener,
) -> None:
    listener.on_terrain_changed(scene)


def _notify_tree_cut(
    scene: GameScene, event: TreeCutEvent, listener: TreeCutListener
) -> None:
    listener.on_tree_cut(scene)


def _after_delete(scene: GameScene, event: Delete) -> None:
    scene.cm.delete(event.entity)


def _after_die(scene: GameScene, event: Die) -> None:
    scene.cm.delete(event.entity)


def _after_quit_game(scene: GameScene, event: QuitGame) -> None:
    if scene.config.autosave_enabled:
        save_game(scene, SaveGame(entity=scene.player))
    scene.pop()
    scene.controller.push_scene(get_start_menu())


def _after_step_event(scene: GameScene, event: StepEvent) -> None:
    # emit entered events
    this_coords = scene.cm.get_one(Coordinates, entity=event.entity)
    enter_listeners = scene.cm.get(EnterListener)
    for enter_listener in enter_listeners:
        other_coords = scene.cm.get_one(
            Coordinates, entity=enter_listener.entity
        )
        if this_coords.is_at(other_coords):
            scene.cm.add(
                EnterEvent(entity=event.entity, entered=enter_listener.entity)
            )


EVENT_LISTENERS: Dict[Type[Component], EventDispatchRule] = {
    AttackFinished: EventDispatchRule(
        listener_type=OnAttackFinishedListener, notify=_notify_attack_finished
    ),
    DallyEvent: EventDispatchRule(
        listener_type=None, notify=None, consume=False
    ),
    DayBegan: EventDispatchRule(
        listener_type=DayBeganListener, notify=_notify_day_began
    ),
    Delete: EventDispatchRule(
        listener_type=DeleteListener,
        notify=_notify_delete,
        after_notify=_after_delete,
    ),
    Die: EventDispatchRule(
        listener_type=None,
        notify=None,
        after_notify=_after_die,
    ),
    EnterEvent: EventDispatchRule(
        listener_type=None, notify=None, consume=False
    ),
    PeasantAdded: EventDispatchRule(
        listener_type=PeasantAddedListener, notify=_notify_peasant_added
    ),
    PeasantDied: EventDispatchRule(
        listener_type=PeasantDiedListener, notify=_notify_peasant_died
    ),
    QuitGame: EventDispatchRule(
        listener_type=QuitGameListener,
        notify=_notify_quit_game,
        after_remove=_after_quit_game,
    ),
    StartGame: EventDispatchRule(
        listener_type=GameStartListener, notify=_notify_start_game
    ),
    StepEvent: EventDispatchRule(
        listener_type=None,
        notify=None,
        after_notify=_after_step_event,
        consume=False,
    ),
    TerrainChangedEvent: EventDispatchRule(
        listener_type=TerrainChangedListener,
        notify=_notify_terrain_changed,
    ),
    TreeCutEvent: EventDispatchRule(
        listener_type=TreeCutListener, notify=_notify_tree_cut
    ),
}


def _dispatch_event(
    scene: GameScene, event: Component, rule: EventDispatchRule
) -> None:
    if rule.listener_type and rule.notify:
        for listener in scene.cm.get(rule.listener_type):
            rule.notify(scene, event, listener)
    if rule.after_notify:
        rule.after_notify(scene, event)
    if rule.consume:
        scene.cm.delete_component(event)
        if rule.after_remove:
            rule.after_remove(scene, event)


def run(scene: GameScene) -> None:
    """
    Dispatch all events currently queued in the component manager.

    Args:
        scene: Scene providing the component manager used for dispatch.

    Side Effects:
        - Notifies event listeners.
        - Removes dispatched event components from the component manager,
          except for movement events that are handled elsewhere.

    """
    for event_type, rule in EVENT_LISTENERS.items():
        for event in list(scene.cm.get(event_type)):
            _dispatch_event(scene, event, rule)
