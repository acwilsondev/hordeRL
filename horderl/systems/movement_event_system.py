"""System for handling movement-related events and their effects."""

from __future__ import annotations

from engine import GameScene
from engine.components import Coordinates
from horderl import palettes
from horderl.components import Attributes
from horderl.components.actions.attack_action import AttackAction
from horderl.components.events.dally_event import DallyEvent
from horderl.components.events.die_events import Die
from horderl.components.events.step_event import EnterEvent, StepEvent
from horderl.components.movement.die_on_enter import DieOnEnter
from horderl.components.movement.drain_on_enter import DrainOnEnter
from horderl.components.movement.heal_on_dally import HealOnDally
from horderl.components.movement.pickup_gold import PickupGoldOnStep
from horderl.components.pickup_gold import GoldPickup


def run(scene: GameScene) -> None:
    """
    Process movement-related events and apply their side effects.

    Args:
        scene: Active game scene providing component manager access.

    Side Effects:
        - Adds AttackAction and Die events for enter effects.
        - Updates gold totals and message log for pickups.
        - Updates health for dally-based healing.
        - Removes processed movement events.

    """
    for event in list(scene.cm.get(StepEvent)):
        _handle_step_event(scene, event)
        scene.cm.delete_component(event)

    for event in list(scene.cm.get(EnterEvent)):
        _handle_enter_event(scene, event)
        scene.cm.delete_component(event)

    for event in list(scene.cm.get(DallyEvent)):
        _handle_dally_event(scene, event)
        scene.cm.delete_component(event)


def _handle_step_event(scene: GameScene, event: StepEvent) -> None:
    pickup_listener = scene.cm.get_one(PickupGoldOnStep, entity=event.entity)
    if not pickup_listener:
        return
    _pickup_gold(scene, event.new_location)


def _pickup_gold(scene: GameScene, point: tuple[int, int]) -> None:
    # Gold pickups are removed as soon as they're collected to avoid repeats.
    for pickup in list(scene.cm.get(GoldPickup)):
        gold_coords = scene.cm.get_one(Coordinates, entity=pickup.entity)
        if gold_coords and gold_coords.is_at_point(point):
            scene.cm.delete(pickup.entity)
            scene.gold += pickup.amount
            scene.message(
                f"You found {pickup.amount} gold.", color=palettes.GOLD
            )


def _handle_enter_event(scene: GameScene, event: EnterEvent) -> None:
    drain_on_enter = scene.cm.get_one(DrainOnEnter, entity=event.entered)
    if drain_on_enter:
        scene.cm.add(
            AttackAction(
                entity=event.entered,
                target=event.entity,
                damage=drain_on_enter.damage,
            )
        )

    die_on_enter = scene.cm.get_one(DieOnEnter, entity=event.entered)
    if die_on_enter:
        scene.cm.add(Die(entity=event.entered, killer=event.entity))


def _handle_dally_event(scene: GameScene, event: DallyEvent) -> None:
    healer = scene.cm.get_one(HealOnDally, entity=event.entity)
    if not healer:
        return

    healer.count = (healer.count + 1) % healer.heal_count
    if healer.count != 0:
        return

    attributes = scene.cm.get_one(Attributes, entity=event.entity)
    if not attributes:
        return

    if attributes.hp < attributes.max_hp:
        attributes.hp = min(attributes.hp + 1, attributes.max_hp)
        scene.message("You rest and your wounds heal.", color=palettes.WHITE)
