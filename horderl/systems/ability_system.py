from __future__ import annotations

from math import sqrt
from typing import Callable

from engine.components import Coordinates
from engine.logging import get_logger
from engine.utilities import is_visible
from horderl import palettes
from horderl.components.abilities.ability import Ability
from horderl.components.abilities.control_mode_ability import (
    ControlModeAbility,
)
from horderl.components.abilities.debug_ability import DebugAbility
from horderl.components.abilities.look_ability import LookAbility
from horderl.components.abilities.null_ability import NullAbility
from horderl.components.abilities.shoot_ability import ShootAbility
from horderl.components.abilities.thwack_ability import ThwackAbility
from horderl.components.actions.attack_action import AttackAction
from horderl.components.animation_definitions.blinker_animation_definition import (
    BlinkerAnimationDefinition,
)
from horderl.components.brains.ability_actors.dig_hole_actor import (
    DigHoleActor,
)
from horderl.components.brains.ability_actors.hire_knight_brain import (
    HireKnightActor,
)
from horderl.components.brains.ability_actors.look_cursor_controller import (
    LookCursorController,
)
from horderl.components.brains.ability_actors.place_bomb_actor import (
    PlaceBombActor,
)
from horderl.components.brains.ability_actors.place_cow_actor import (
    PlaceCowActor,
)
from horderl.components.brains.ability_actors.place_fence_actor import (
    PlaceFenceActor,
)
from horderl.components.brains.ability_actors.place_haunch_actor import (
    PlaceHaunchActor,
)
from horderl.components.brains.ability_actors.place_spikes_actor import (
    PlaceSpikesActor,
)
from horderl.components.brains.ability_actors.place_stone_wall_actor import (
    PlaceStoneWallActor,
)
from horderl.components.brains.ability_actors.plant_sapling_actor import (
    PlaceSaplingActor,
)
from horderl.components.brains.ability_actors.ranged_attack_actor import (
    RangedAttackActor,
)
from horderl.components.brains.ability_actors.sell_thing_actor import (
    SellThingActor,
)
from horderl.components.brains.fast_forward_actor import FastForwardBrain
from horderl.components.tags.tag import Tag, TagType
from horderl.components.wants_to_show_debug import WantsToShowDebug
from horderl.content.attacks import thwack_animation, thwack_dizzy_animation
from horderl.content.cursor import make_cursor
from horderl.content.states import confused_animation, no_money_animation
from horderl.i18n import t
from horderl.systems import brain_stack
from horderl.systems.utilities import get_current_turn, get_enemies_in_range

AbilityHandler = Callable[[object, int, Ability], None]

_ABILITY_HANDLERS: dict[type[Ability], AbilityHandler] = {}
_CONTROL_MODE_ACTORS: dict[str, type] = {
    "dig_hole": DigHoleActor,
    "fast_forward": FastForwardBrain,
    "hire_knight": HireKnightActor,
    "place_bomb": PlaceBombActor,
    "place_cow": PlaceCowActor,
    "place_fence": PlaceFenceActor,
    "place_haunch": PlaceHaunchActor,
    "place_sapling": PlaceSaplingActor,
    "place_spikes": PlaceSpikesActor,
    "place_stone_wall": PlaceStoneWallActor,
    "sell": SellThingActor,
}


def run(scene) -> None:
    """
    Update ability state that requires per-tick processing.

    Args:
        scene: Active game scene.

    Side effects:
        - Advances recharge counters for abilities such as Thwack.
    """
    _recharge_thwack(scene)


def apply_ability(scene, dispatcher_id: int, ability: Ability) -> None:
    """
    Apply an ability, enforcing costs before dispatching behavior.

    Args:
        scene: Active game scene.
        dispatcher_id: Component ID for the current controller/brain.
        ability: The ability component being executed.

    Side effects:
        - Emits warnings/animations for insufficient gold.
        - Dispatches ability-specific behavior on success.
    """
    if scene.gold < ability.use_cost:
        _handle_no_money(scene, ability)
        return
    _dispatch_ability(scene, dispatcher_id, ability)


def _handle_no_money(scene, ability: Ability) -> None:
    # Assumes the ability owner has coordinates for the animation.
    scene.warn(t("warning.no_money"))
    player_coords = scene.cm.get_one(Coordinates, entity=ability.entity)
    confused_anim = no_money_animation(player_coords.x, player_coords.y)
    scene.cm.add(*confused_anim[1])


def _dispatch_ability(scene, dispatcher_id: int, ability: Ability) -> None:
    if isinstance(ability, ControlModeAbility):
        _apply_control_mode(scene, dispatcher_id, ability)
        return

    handler = _ABILITY_HANDLERS.get(type(ability))
    if handler:
        handler(scene, dispatcher_id, ability)
        return

    logger = get_logger(__name__)
    logger.warning(
        "No ability handler registered",
        extra={"entity": ability.entity, "ability": type(ability).__name__},
    )


def _apply_control_mode(
    scene, dispatcher_id: int, ability: ControlModeAbility
) -> None:
    logger = get_logger(__name__)
    logger.debug(
        "Switching control mode",
        extra={
            "entity": ability.entity,
            "ability": type(ability).__name__,
            "dispatcher": dispatcher_id,
        },
    )
    mode_factory = _CONTROL_MODE_ACTORS.get(ability.control_mode_key)
    if mode_factory is None:
        logger.warning(
            "Unknown control mode key",
            extra={
                "entity": ability.entity,
                "ability": type(ability).__name__,
                "control_mode_key": ability.control_mode_key,
            },
        )
        return
    new_controller = mode_factory(
        entity=ability.entity, old_brain=dispatcher_id
    )
    blinker = BlinkerAnimationDefinition(
        entity=ability.entity,
        new_symbol=ability.anim_symbol,
        new_color=ability.anim_color,
    )
    scene.cm.stash_component(dispatcher_id)
    scene.cm.add(new_controller, blinker)


def _apply_debug(scene, _dispatcher_id: int, ability: DebugAbility) -> None:
    scene.cm.add(WantsToShowDebug(entity=ability.entity))


def _apply_look(scene, dispatcher_id: int, ability: LookAbility) -> None:
    coords = scene.cm.get_one(Coordinates, entity=ability.entity)
    cursor = make_cursor(coords.x, coords.y)
    scene.cm.add(
        LookCursorController(
            entity=ability.entity, old_brain=dispatcher_id, cursor=cursor[0]
        )
    )
    scene.cm.add(*cursor[1])
    scene.cm.stash_component(dispatcher_id)


def _apply_null(scene, _dispatcher_id: int, _ability: NullAbility) -> None:
    return


def _apply_shoot(scene, dispatcher_id: int, ability: ShootAbility) -> None:
    hordelings = [
        tag
        for tag in scene.cm.get(
            Tag, query=lambda tag: tag.tag_type == TagType.HORDELING
        )
        if is_visible(scene, scene.cm.get_one(Coordinates, entity=tag.entity))
    ]
    if not hordelings:
        _handle_confused(scene, ability)
        return
    _handle_shoot(scene, hordelings, dispatcher_id, ability)


def _handle_shoot(
    scene,
    hordelings: list[Tag],
    dispatcher_id: int,
    ability: ShootAbility,
) -> None:
    target = hordelings[0]
    new_controller = RangedAttackActor(
        entity=ability.entity,
        old_actor=dispatcher_id,
        target=target.entity,
        shoot_ability=ability.id,
    )
    blinker = BlinkerAnimationDefinition(entity=target.entity)
    scene.cm.stash_component(dispatcher_id)
    scene.cm.add(new_controller, blinker)
    scene.gold -= ability.use_cost


def _handle_confused(scene, ability: Ability) -> None:
    player_coords = scene.cm.get_one(Coordinates, entity=ability.entity)
    confused_anim = confused_animation(player_coords.x, player_coords.y)
    scene.cm.add(*confused_anim[1])


def _apply_thwack(scene, dispatcher_id: int, ability: ThwackAbility) -> None:
    current_turn = get_current_turn(scene)
    if ability.count > 0:
        ability.is_recharging = True
        ability.count -= 1

        thwackables = get_enemies_in_range(
            scene, ability.entity, max_range=sqrt(2)
        )
        attacks = [
            AttackAction(entity=ability.entity, target=target, damage=1)
            for target in thwackables
        ]
        for attack in attacks:
            scene.cm.add(attack)

        thwacker_coords = scene.cm.get_one(Coordinates, entity=ability.entity)
        if ability.count > 0:
            scene.cm.add(
                *thwack_animation(
                    ability.entity, thwacker_coords.x, thwacker_coords.y
                )[1]
            )
        else:
            scene.warn(t("warning.thwack_dizzy"))
            scene.cm.add(
                *thwack_dizzy_animation(
                    ability.entity, thwacker_coords.x, thwacker_coords.y
                )[1]
            )

    brain = scene.cm.get_component_by_id(dispatcher_id)
    if brain:
        brain.pass_turn(current_turn)
    ability.pass_turn(current_turn)

    if ability.count <= 0:
        _apply_dizzy(scene, ability)


def _apply_dizzy(scene, ability: ThwackAbility) -> None:
    from horderl.components.brains.dizzy_brain import DizzyBrain

    brain_stack.swap(scene, ability.entity, DizzyBrain(entity=ability.entity))
    scene.cm.add(
        BlinkerAnimationDefinition(
            entity=ability.entity,
            new_symbol="?",
            new_color=palettes.LIGHT_WATER,
        )
    )


def _recharge_thwack(scene) -> None:
    current_turn = get_current_turn(scene)
    for ability in scene.cm.get(ThwackAbility):
        if ability.can_act(current_turn):
            ability._log_debug("recovering from thwack")
            ability.count = min(ability.max, ability.count + 1)
            ability.is_recharging = ability.count < ability.max
            ability.pass_turn(current_turn)


_ABILITY_HANDLERS.update(
    {
        DebugAbility: _apply_debug,
        LookAbility: _apply_look,
        NullAbility: _apply_null,
        ShootAbility: _apply_shoot,
        ThwackAbility: _apply_thwack,
    }
)
