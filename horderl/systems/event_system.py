"""System for dispatching event components to handler functions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional, Type

from engine import GameScene, core
from engine.components import Coordinates
from engine.components.component import Component
from engine.logging import get_logger
from horderl import palettes
from horderl.components.actors.calendar_actor import Calendar
from horderl.components.announce_game_start import AnnounceGameStart
from horderl.components.die_on_attack_finished import DieOnAttackFinished
from horderl.components.events.attack_events import (
    AttackFinished,
    OnAttackFinishedListener,
)
from horderl.components.events.dally_event import DallyEvent
from horderl.components.events.delete_event import Delete, DeleteListener
from horderl.components.events.die_events import Die
from horderl.components.events.fast_forward import FastForward
from horderl.components.events.new_day_event import DayBegan, DayBeganListener
from horderl.components.events.peasant_events import (
    PeasantAdded,
    PeasantAddedListener,
    PeasantDied,
    PeasantDiedListener,
)
from horderl.components.events.popup_message import PopupMessage
from horderl.components.events.quit_game_events import (
    QuitGame,
    QuitGameListener,
)
from horderl.components.events.show_help_dialogue import ShowHelpDialogue
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
from horderl.components.population import Population
from horderl.components.season_reset_listeners.grow_in_spring import (
    GrowIntoTree,
)
from horderl.components.serialization.save_game import SaveGame
from horderl.components.weather.weather import Weather
from horderl.components.world_beauty import WorldBeauty
from horderl.components.world_building.world_parameters import WorldParameters
from horderl.content.terrain.trees import make_tree
from horderl.gui.help_dialogue import HelpDialogue
from horderl.i18n import t
from horderl.scenes.start_menu import get_start_menu
from horderl.systems.serialization_system import save_game

EventListenerHandler = Callable[[GameScene, Component, Component], None]
EventHandler = Callable[[GameScene, Component], None]


@dataclass(frozen=True)
class EventDispatchRule:
    """Define how to route an event to handler functions and follow-up actions."""

    listener_type: Optional[Type[Component]] = None
    listener_handlers: Optional[
        Dict[Type[Component], EventListenerHandler]
    ] = None
    handle_event: Optional[EventHandler] = None
    after_notify: Optional[EventHandler] = None
    after_remove: Optional[EventHandler] = None
    consume: bool = True


def _notify_listeners(
    scene: GameScene,
    event: Component,
    listener_type: Type[Component],
    handlers: Dict[Type[Component], EventListenerHandler],
) -> None:
    # Allow handler lookup by base type to support subclasses.
    for listener in scene.cm.get(listener_type):
        for handled_type, handler in handlers.items():
            if isinstance(listener, handled_type):
                handler(scene, event, listener)


def _handle_popup_message(scene: GameScene, event: PopupMessage) -> None:
    if event.next_update:
        scene.popup_message(event.message)
        scene.cm.delete_component(event)


def _handle_fast_forward(scene: GameScene, event: FastForward) -> None:
    logger = get_logger(__name__)
    logger.debug(
        "Fast-forwarding calendar",
        extra={"entity": event.entity, "target_day": 30},
    )
    calendar = scene.cm.get_one(Calendar, entity=core.get_id("calendar"))
    if calendar:
        calendar.day = 30
        calendar.energy = 0
        scene.cm.add(DayBegan(entity=core.get_id("calendar"), day=30))


def _handle_show_help_dialogue(
    scene: GameScene, event: ShowHelpDialogue
) -> None:
    messages = [
        t("help.dialogue.intro"),
        t("help.dialogue.controls"),
        t("help.dialogue.money"),
        t("help.dialogue.money_pt2"),
        t("help.dialogue.attacks"),
    ]
    if hasattr(scene, "message"):
        for message in messages:
            scene.message(message)
    scene.add_gui_element(HelpDialogue(messages, scene.config))


def _notify_attack_finished(
    scene: GameScene, event: AttackFinished, listener: DieOnAttackFinished
) -> None:
    if event.entity == listener.entity:
        scene.cm.add(Die(entity=listener.entity))


def _notify_day_began(
    scene: GameScene, event: DayBegan, listener: GrowIntoTree
) -> None:
    weather_list = scene.cm.get(Weather)
    if weather_list:
        weather = weather_list[0]
    else:
        listener._log_warning("no weather found")
        return

    listener.time_to_grow = max(
        0, listener.time_to_grow - max(0, weather.temperature)
    )

    if listener.time_to_grow <= 0:
        listener._log_debug("sapling growing into a tree")
        coords = scene.cm.get_one(Coordinates, entity=listener.entity)
        x = coords.x
        y = coords.y
        scene.cm.delete(listener.entity)
        scene.cm.add(*make_tree(x, y)[1])


def _notify_peasant_added(
    scene: GameScene, event: PeasantAdded, listener: Population
) -> None:
    listener._log_info("population increased")
    listener.population += 1


def _notify_peasant_died(
    scene: GameScene, event: PeasantDied, listener: Population
) -> None:
    listener._log_info("population decreased")
    listener.population -= 1
    if listener.population <= 0:
        scene.popup_message(t("message.peasants_dead"))
        scene.pop()


def _notify_start_game(
    scene: GameScene, event: StartGame, listener: AnnounceGameStart
) -> None:
    scene.message(t("message.start.protect"))
    scene.message(t("message.start.horde"))
    scene.message(t("message.start.help"))
    scene.cm.delete_component(listener)


def _notify_tree_cut(
    scene: GameScene, event: TreeCutEvent, listener: WorldBeauty
) -> None:
    listener._log_info("detected tree cut")
    listener.trees_cut += 1
    if not listener.trees_cut % listener.spirits_attitude:
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
    # Emit entered events after stepping, relying on movement system to consume.
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


EVENT_RULES: Dict[Type[Component], EventDispatchRule] = {
    AttackFinished: EventDispatchRule(
        listener_type=OnAttackFinishedListener,
        listener_handlers={DieOnAttackFinished: _notify_attack_finished},
    ),
    DallyEvent: EventDispatchRule(listener_type=None, consume=False),
    DayBegan: EventDispatchRule(
        listener_type=DayBeganListener,
        listener_handlers={GrowIntoTree: _notify_day_began},
    ),
    Delete: EventDispatchRule(
        listener_type=DeleteListener,
        after_notify=_after_delete,
    ),
    Die: EventDispatchRule(
        listener_type=None,
        after_notify=_after_die,
    ),
    EnterEvent: EventDispatchRule(listener_type=None, consume=False),
    FastForward: EventDispatchRule(handle_event=_handle_fast_forward),
    PeasantAdded: EventDispatchRule(
        listener_type=PeasantAddedListener,
        listener_handlers={Population: _notify_peasant_added},
    ),
    PeasantDied: EventDispatchRule(
        listener_type=PeasantDiedListener,
        listener_handlers={Population: _notify_peasant_died},
    ),
    PopupMessage: EventDispatchRule(
        handle_event=_handle_popup_message, consume=False
    ),
    QuitGame: EventDispatchRule(
        listener_type=QuitGameListener,
        after_remove=_after_quit_game,
    ),
    ShowHelpDialogue: EventDispatchRule(
        handle_event=_handle_show_help_dialogue
    ),
    StartGame: EventDispatchRule(
        listener_type=GameStartListener,
        listener_handlers={AnnounceGameStart: _notify_start_game},
    ),
    StepEvent: EventDispatchRule(
        listener_type=None,
        after_notify=_after_step_event,
        consume=False,
    ),
    TerrainChangedEvent: EventDispatchRule(
        listener_type=TerrainChangedListener
    ),
    TreeCutEvent: EventDispatchRule(
        listener_type=TreeCutListener,
        listener_handlers={WorldBeauty: _notify_tree_cut},
    ),
}


def _dispatch_event(
    scene: GameScene, event: Component, rule: EventDispatchRule
) -> None:
    if rule.handle_event:
        rule.handle_event(scene, event)
    if rule.listener_type and rule.listener_handlers:
        _notify_listeners(
            scene, event, rule.listener_type, rule.listener_handlers
        )
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
        - Notifies event handler functions.
        - Removes dispatched event components from the component manager,
          except for movement events handled elsewhere.

    """
    for event_type, rule in EVENT_RULES.items():
        for event in list(scene.cm.get(event_type)):
            _dispatch_event(scene, event, rule)
