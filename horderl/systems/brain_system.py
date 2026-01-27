"""System routines for brain-driven actor behavior."""

import random
from typing import List, Optional

import tcod

from engine import constants, core, utilities
from engine.components import Coordinates
from engine.logging import get_logger
from engine.utilities import is_visible
from horderl import palettes
from horderl.components.ability_tracker import AbilityTracker
from horderl.components.actions.attack_action import AttackAction
from horderl.components.actions.eat_action import EatAction
from horderl.components.actions.tunnel_to_point import TunnelToPoint
from horderl.components.actors import STEP_VECTOR_MAP, STEPS, VECTOR_STEP_MAP
from horderl.components.animation_definitions.blinker_animation_definition import (
    BlinkerAnimationDefinition,
)
from horderl.components.attacks.attack import Attack
from horderl.components.brains.ability_actors.dig_hole_actor import (
    DigHoleActor,
)
from horderl.components.brains.ability_actors.look_cursor_controller import (
    LookCursorController,
)
from horderl.components.brains.ability_actors.place_thing_actor import (
    PlaceThingActor,
)
from horderl.components.brains.ability_actors.ranged_attack_actor import (
    RangedAttackActor,
)
from horderl.components.brains.ability_actors.sell_thing_actor import (
    SellThingActor,
)
from horderl.components.brains.brain import Brain
from horderl.components.brains.default_active_actor import DefaultActiveActor
from horderl.components.brains.dizzy_brain import DizzyBrain
from horderl.components.brains.fast_forward_actor import FastForwardBrain
from horderl.components.brains.painters.painter_brain import PainterBrain
from horderl.components.brains.peasant_actor import PeasantActor
from horderl.components.brains.player_brain import PlayerBrain
from horderl.components.brains.player_dead_actor import PlayerDeadBrain
from horderl.components.brains.sleeping_brain import SleepingBrain
from horderl.components.brains.stationary_attack_actor import (
    StationaryAttackActor,
)
from horderl.components.diggable import Diggable
from horderl.components.edible import Edible
from horderl.components.enums import Intention
from horderl.components.events.breadcrumb_events import BreadcrumbsRequested
from horderl.components.events.die_events import Die
from horderl.components.events.peasant_events import PeasantDied
from horderl.components.events.quit_game_events import QuitGame
from horderl.components.events.show_help_dialogue import ShowHelpDialogue
from horderl.components.pathfinding.breadcrumb_tracker import BreadcrumbTracker
from horderl.components.pathfinding.cost_mapper import CostMapper
from horderl.components.pathfinding.target_evaluation.target_evaluator import (
    TargetEvaluator,
    TargetEvaluatorType,
)
from horderl.components.sellable import Sellable
from horderl.components.stomach import Stomach
from horderl.components.tags.tag import Tag, TagType
from horderl.content.attacks import stab
from horderl.content.states import confused_animation, sleep_animation
from horderl.content.terrain import roads
from horderl.content.terrain.dirt import make_dirt
from horderl.content.terrain.hole import make_hole
from horderl.systems.abilities import (
    ability_selection_system,
    placement_system,
)
from horderl.systems.debug import painter_system
from horderl.systems.pathfinding import get_path
from horderl.systems.pathfinding.target_selection import (
    get_cost_map,
    get_new_target,
    get_target_values,
)
from horderl.systems.stomach_system import clear_stomach
from horderl.systems.utilities import get_current_turn

BRAIN_HANDLERS = (
    (LookCursorController, "run_look_cursor_controller"),
    (DigHoleActor, "run_dig_hole_actor"),
    (RangedAttackActor, "run_ranged_attack_actor"),
    (SellThingActor, "run_sell_thing_actor"),
    (PlaceThingActor, "run_place_thing_actor"),
    (PainterBrain, "run_painter_brain"),
    (DefaultActiveActor, "run_default_active_actor"),
    (StationaryAttackActor, "run_stationary_attack_actor"),
    (PeasantActor, "run_peasant_actor"),
    (PlayerDeadBrain, "run_player_dead_brain"),
    (PlayerBrain, "run_player_brain"),
    (DizzyBrain, "run_dizzy_brain"),
    (FastForwardBrain, "run_fast_forward_brain"),
    (SleepingBrain, "run_sleeping_brain"),
)


def run(scene) -> None:
    """
    Run all active brain components for the current scene.

    Args:
        scene: Active scene containing component manager and config.

    Side Effects:
        - Advances AI or input-driven brain state.
        - Enqueues actions, events, or animations.
    """
    for brain in get_active_brains(scene):
        run_brain(scene, brain)


def _entity_has_tag(scene, entity: int, tag_type: TagType) -> bool:
    # Assumes entities may have zero or multiple tag components.
    return any(
        tag.tag_type == tag_type
        for tag in scene.cm.get_all(Tag, entity=entity)
    )


def get_active_brains(scene) -> List[Brain]:
    """
    Collect brains that are ready to act.

    Args:
        scene: Active scene containing component manager.

    Returns:
        List[Brain]: Active brain components that can act.
    """
    current_turn = get_current_turn(scene)
    return [
        brain for brain in scene.cm.get(Brain) if brain.can_act(current_turn)
    ]


def run_brain(scene, brain: Brain) -> None:
    """
    Dispatch a brain component to its behavior handler.

    Args:
        scene: Active scene containing component manager and config.
        brain: Brain component to execute.

    Side Effects:
        - Triggers brain-specific logic depending on the component type.
    """
    for brain_type, handler_name in BRAIN_HANDLERS:
        if isinstance(brain, brain_type):
            handler = globals()[handler_name]
            handler(scene, brain)
            return
    get_logger(__name__).warning(
        "No brain handler registered",
        extra={"entity": brain.entity, "brain_type": type(brain).__name__},
    )


def run_default_active_actor(scene, brain: DefaultActiveActor) -> None:
    """
    Execute the default hostile AI behavior for a brain.

    Args:
        scene: Active scene containing component manager and config.
        brain: DefaultActiveActor component for the entity.

    Side Effects:
        - Updates target selection and intention.
        - Adds attack/eat/tunnel actions or death events.
        - Consumes time via pass_turn().
    """
    logger = get_logger(__name__)
    logger.debug(
        "Default active actor tick",
        extra={"entity": brain.entity, "target": brain.target},
    )
    brain.cost_map = _get_cost_map(scene, brain)

    target_evaluator = scene.cm.get_one(TargetEvaluator, entity=brain.entity)
    if not target_evaluator:
        brain._log_warning("missing target evaluator")
        target_evaluator = TargetEvaluator(
            evaluator_type=TargetEvaluatorType.HORDELING
        )

    entity_values = get_target_values(scene, target_evaluator)

    if not entity_values:
        brain.pass_turn(get_current_turn(scene))
        return

    coords = scene.cm.get_one(Coordinates, entity=brain.entity)
    brain.target = get_new_target(
        scene, brain.cost_map, (coords.x, coords.y), entity_values
    )

    if _is_target_in_range(scene, brain):
        if _should_eat(scene, brain):
            _eat_target(scene, brain)
        else:
            _attack_target(scene, brain)
    else:
        _move_towards_target(scene, brain)


def run_stationary_attack_actor(scene, brain: StationaryAttackActor) -> None:
    """
    Execute the stationary attacker behavior.

    Args:
        scene: Active scene containing component manager and config.
        brain: StationaryAttackActor component for the entity.

    Side Effects:
        - Selects a nearby target and attacks.
        - Consumes time via pass_turn().
    """
    logger = get_logger(__name__)
    logger.debug(
        "Stationary attacker tick",
        extra={"entity": brain.entity, "root": (brain.root_x, brain.root_y)},
    )
    coords = scene.cm.get_one(Coordinates, entity=brain.entity)
    targets = scene.cm.get(
        Coordinates,
        query=lambda c: _entity_has_tag(scene, c.entity, TagType.HORDELING)
        and c.distance_from(coords) <= 2,
        project=lambda c: c.entity,
    )
    if not targets:
        brain.pass_turn(get_current_turn(scene))
        return
    brain.target = targets.pop()
    _attack_stationary_target(scene, brain)


def run_peasant_actor(scene, brain: PeasantActor) -> None:
    """
    Execute one peasant behavior tick.

    Args:
        scene: Active scene containing component manager and config.
        brain: PeasantActor component for the entity.

    Side Effects:
        - Updates intention or consumes time via pass_turn().
    """
    logger = get_logger(__name__)
    logger.debug(
        "Peasant actor tick",
        extra={"entity": brain.entity, "state": brain.state.value},
    )
    if brain.state is PeasantActor.State.FARMING:
        _farm(scene, brain)
    elif brain.state is PeasantActor.State.WANDERING:
        _wander(scene, brain)
    else:
        brain.pass_turn(get_current_turn(scene))


def run_player_brain(scene, brain: PlayerBrain) -> None:
    """
    Execute the player brain input handling.

    Args:
        scene: Active scene containing component manager and input state.
        brain: PlayerBrain component for the entity.

    Side Effects:
        - Updates intentions and triggers abilities or UI events.
    """
    _handle_player_input(scene, brain, PLAYER_KEY_ACTION_MAP)


def run_dizzy_brain(scene, brain: DizzyBrain) -> None:
    """
    Execute the dizzy brain input handling.

    Args:
        scene: Active scene containing component manager and input state.
        brain: DizzyBrain component for the entity.

    Side Effects:
        - Updates intention randomly after input.
        - Adds confusion animations.
    """
    _handle_dizzy_input(scene, brain, DIZZY_KEY_ACTION_MAP)


def run_fast_forward_brain(scene, brain: FastForwardBrain) -> None:
    """
    Execute fast-forward input handling.

    Args:
        scene: Active scene containing component manager and input state.
        brain: FastForwardBrain component for the entity.

    Side Effects:
        - Updates intention or backs out the brain.
    """
    _handle_fast_forward_input(scene, brain, FAST_FORWARD_KEY_ACTION_MAP)


def run_sleeping_brain(scene, brain: SleepingBrain) -> None:
    """
    Execute the sleeping brain tick.

    Args:
        scene: Active scene containing component manager and config.
        brain: SleepingBrain component for the entity.

    Side Effects:
        - Adds sleep animations.
        - Consumes time via pass_turn().
        - Pops brain stack when finished.
    """
    logger = get_logger(__name__)
    logger.debug(
        "Sleeping brain tick",
        extra={"entity": brain.entity, "turns_remaining": brain.turns},
    )
    brain._log_debug("sleeping one turn")
    coords = scene.cm.get_one(Coordinates, entity=brain.entity)
    scene.cm.add(*sleep_animation(coords.x, coords.y)[1])
    brain.pass_turn(get_current_turn(scene))
    if brain.turns <= 0:
        from horderl.systems import brain_stack

        brain_stack.back_out(scene, brain)
    else:
        brain.turns -= 1


def run_player_dead_brain(scene, brain: PlayerDeadBrain) -> None:
    """
    Execute the player-dead brain input handling.

    Args:
        scene: Active scene containing component manager and input state.
        brain: PlayerDeadBrain component for the entity.

    Side Effects:
        - Updates ability selection or triggers warning messages.
    """
    _handle_player_dead_input(scene, brain, PLAYER_DEAD_KEY_ACTION_MAP)


def run_painter_brain(scene, brain: PainterBrain) -> None:
    """
    Execute the debug painter brain input handling.

    Args:
        scene: Active scene containing component manager and input state.
        brain: PainterBrain component for the entity.

    Side Effects:
        - Moves cursor, paints content, or exits painter mode.
    """
    key_event = core.get_key_event()
    if key_event:
        key_event = key_event.sym
        intention = PAINTER_KEY_ACTION_MAP.get(key_event, None)
        if intention in {
            Intention.STEP_NORTH,
            Intention.STEP_EAST,
            Intention.STEP_WEST,
            Intention.STEP_SOUTH,
        }:
            _move_cursor(scene, brain, intention)
        if intention is Intention.USE_ABILITY:
            _paint(scene, brain)
        elif intention is Intention.BACK:
            scene.cm.delete(brain.cursor)
            from horderl.systems import brain_stack

            brain_stack.back_out(scene, brain)


def run_look_cursor_controller(scene, brain: LookCursorController) -> None:
    """
    Execute the look cursor controller input handling.

    Args:
        scene: Active scene containing component manager and input state.
        brain: LookCursorController component for the entity.

    Side Effects:
        - Moves cursor, shows descriptions, or exits look mode.
    """
    key_event = core.get_key_event()
    if key_event:
        key_event = key_event.sym
        intention = LOOK_CURSOR_KEY_ACTION_MAP.get(key_event, None)
        if intention in {
            Intention.STEP_NORTH,
            Intention.STEP_EAST,
            Intention.STEP_WEST,
            Intention.STEP_SOUTH,
        }:
            _move_cursor(scene, brain, intention)
        if intention is Intention.USE_ABILITY:
            _handle_look(scene, brain)
        elif intention is Intention.BACK:
            scene.cm.delete(brain.cursor)
            from horderl.systems import brain_stack

            brain_stack.back_out(scene, brain)


def run_place_thing_actor(scene, brain: PlaceThingActor) -> None:
    """
    Execute a placement ability actor.

    Args:
        scene: Active scene containing component manager and input state.
        brain: PlaceThingActor component for the entity.

    Side Effects:
        - Places a buildable object and spends gold.
        - Consumes time via pass_turn() after placement.
    """
    key_event = core.get_key_event()
    if key_event:
        key_event = key_event.sym
        intention = PLACE_THING_KEY_ACTION_MAP.get(key_event, None)
        if intention in {
            Intention.STEP_NORTH,
            Intention.STEP_EAST,
            Intention.STEP_WEST,
            Intention.STEP_SOUTH,
        }:
            _place_thing(scene, brain, intention)
        elif intention is Intention.BACK:
            from horderl.systems import brain_stack

            brain_stack.back_out(scene, brain)


def run_dig_hole_actor(scene, brain: DigHoleActor) -> None:
    """
    Execute the dig hole ability actor.

    Args:
        scene: Active scene containing component manager and input state.
        brain: DigHoleActor component for the entity.

    Side Effects:
        - Creates holes or removes diggable entities.
        - Updates gold and consumes time via pass_turn().
    """
    key_event = core.get_key_event()
    if key_event:
        key_event = key_event.sym
        intention = DIG_HOLE_KEY_ACTION_MAP.get(key_event, None)
        if intention in {
            Intention.STEP_NORTH,
            Intention.STEP_EAST,
            Intention.STEP_WEST,
            Intention.STEP_SOUTH,
        }:
            _dig_hole(scene, brain, intention)
        elif intention is Intention.BACK:
            from horderl.systems import brain_stack

            brain_stack.back_out(scene, brain)


def run_ranged_attack_actor(scene, brain: RangedAttackActor) -> None:
    """
    Execute the ranged attack ability actor.

    Args:
        scene: Active scene containing component manager and input state.
        brain: RangedAttackActor component for the entity.

    Side Effects:
        - Cycles targets or fires attacks.
        - Updates ability counts and brain stack.
    """
    key_event = core.get_key_event()
    if key_event:
        key_event = key_event.sym
        intention = RANGED_ATTACK_KEY_ACTION_MAP.get(key_event, None)
        if intention is Intention.USE_ABILITY:
            _shoot(scene, brain)
        elif intention in {
            Intention.STEP_NORTH,
            Intention.STEP_EAST,
            Intention.STEP_WEST,
            Intention.STEP_SOUTH,
        }:
            _next_enemy(scene, brain)
        elif intention is Intention.BACK:
            _exit_ranged_attack(scene, brain)


def run_sell_thing_actor(scene, brain: SellThingActor) -> None:
    """
    Execute the sell thing ability actor.

    Args:
        scene: Active scene containing component manager and input state.
        brain: SellThingActor component for the entity.

    Side Effects:
        - Sells a sellable entity and updates gold.
        - Consumes time via pass_turn().
    """
    key_event = core.get_key_event()
    if key_event:
        key_event = key_event.sym
        intention = SELL_THING_KEY_ACTION_MAP.get(key_event, None)
        if intention in {
            Intention.STEP_NORTH,
            Intention.STEP_EAST,
            Intention.STEP_WEST,
            Intention.STEP_SOUTH,
        }:
            _sell_thing(scene, brain, intention)
        elif intention is Intention.BACK:
            from horderl.systems import brain_stack

            brain_stack.back_out(scene, brain)


def handle_back_out(scene, brain: Brain) -> None:
    """
    Handle any brain-specific cleanup when backing out of a brain stack.

    Args:
        scene: Active scene containing component manager.
        brain: Brain component that is being removed.

    Side Effects:
        - Performs cleanup such as digestion and messaging for some brains.
    """
    hook = getattr(brain, "_on_back_out", None)
    if callable(hook):
        hook(scene)
    if isinstance(brain, SleepingBrain):
        _handle_sleeping_back_out(scene, brain)


def on_fast_forward_attack_start(scene, brain: FastForwardBrain) -> None:
    """
    Handle attack-start events for fast-forward mode.

    Args:
        scene: Active scene containing component manager.
        brain: FastForwardBrain component for the entity.

    Side Effects:
        - Pops the fast-forward brain off the stack.
    """
    from horderl.systems import brain_stack

    brain_stack.back_out(scene, brain)


def on_stationary_attack_start(scene, brain: StationaryAttackActor) -> None:
    """
    Handle attack-start events for stationary attackers.

    Args:
        scene: Active scene containing component manager.
        brain: StationaryAttackActor component for the entity.

    Side Effects:
        - Teleports the attacker back to its root position.
    """
    _teleport_to_root(scene, brain)


def on_stationary_season_reset(
    scene, brain: StationaryAttackActor, season
) -> None:
    """
    Handle season reset events for stationary attackers.

    Args:
        scene: Active scene containing component manager.
        brain: StationaryAttackActor component for the entity.
        season: Season value triggering the reset.

    Side Effects:
        - Teleports the attacker back to its root position.
    """
    _teleport_to_root(scene, brain)


def _get_cost_map(scene, brain: DefaultActiveActor):
    """# Uses a default cost mapper when none is configured."""
    cost_mapper: Optional[CostMapper] = scene.cm.get_one(
        CostMapper, entity=brain.entity
    )
    return get_cost_map(scene, cost_mapper)


def _move_towards_target(scene, brain: DefaultActiveActor) -> None:
    """# Tunnel as a fallback when no path is available."""
    brain._log_debug(f"stepping towards target {brain.target}")
    coords = scene.cm.get_one(Coordinates, entity=brain.entity)
    next_step_node = _get_next_step(scene, brain)
    if next_step_node is None:
        brain._log_debug("can't find a natural path")
        tunnel_target = _get_emergency_step(scene)
        if tunnel_target:
            scene.cm.add(
                TunnelToPoint(entity=brain.entity, point=tunnel_target)
            )
        else:
            brain._log_warning("can't find a safe place to tunnel to")
            scene.cm.add(Die(entity=brain.entity))
        brain.pass_turn(get_current_turn(scene))
    else:
        next_step = (
            next_step_node[0] - coords.x,
            next_step_node[1] - coords.y,
        )
        brain.intention = VECTOR_STEP_MAP[next_step]
        brain._log_debug(f"set intention {brain.intention}")


def _should_eat(scene, brain: DefaultActiveActor) -> bool:
    """# Eating depends on the target having an Edible component."""
    brain._log_debug(f"checking for edibility of {brain.target}")
    edible = scene.cm.get_one(Edible, entity=brain.target)
    return edible is not None


def _eat_target(scene, brain: DefaultActiveActor) -> None:
    """# Eating transitions to a sleeping brain and consumes a turn."""
    brain._log_debug(f"eating target {brain.target}")
    scene.cm.add(EatAction(entity=brain.entity, target=brain.target))
    edible = scene.cm.get_one(Edible, entity=brain.target)

    _sleep(scene, brain, edible.sleep_for)
    brain.pass_turn(get_current_turn(scene))


def _attack_target(scene, brain: DefaultActiveActor) -> None:
    """# Attacks enqueue animations and consume a turn."""
    brain._log_debug(f"attacking target {brain.target}")

    coords = scene.cm.get_one(Coordinates, entity=brain.entity)
    target = scene.cm.get_one(Coordinates, entity=brain.target)
    facing = coords.direction_towards(target)
    attack = scene.cm.get_one(Attack, entity=brain.entity)
    scene.cm.add(
        AttackAction(
            entity=brain.entity, target=brain.target, damage=attack.damage
        )
    )
    scene.cm.add(
        *stab(brain.entity, coords.x + facing[0], coords.y + facing[1])[1]
    )
    brain.pass_turn(get_current_turn(scene))


def _is_target_in_range(scene, brain: DefaultActiveActor) -> bool:
    """# Range check uses coordinate distance."""
    coords = scene.cm.get_one(Coordinates, entity=brain.entity)
    target = scene.cm.get_one(Coordinates, entity=brain.target)
    return coords.distance_from(target) < 2


def _get_next_step(scene, brain: DefaultActiveActor):
    """# Pathfinding uses breadcrumb tracking when available."""
    self_coords = scene.cm.get_one(Coordinates, entity=brain.entity)
    target_coords = scene.cm.get_one(Coordinates, entity=brain.target)
    path = get_path(
        brain.cost_map, self_coords.position, target_coords.position
    )

    breadcrumb_tracker = scene.cm.get_one(
        BreadcrumbTracker, entity=brain.entity
    )
    if breadcrumb_tracker:
        scene.cm.add(
            BreadcrumbsRequested(entity=brain.entity, path=list(path))
        )

    path = [p for p in path]

    if len(path) <= 1:
        return None
    return path[1]


def _get_emergency_step(scene):
    """# Randomly search open positions that connect to roads."""
    coords = set(scene.cm.get(Coordinates, project=lambda c: c.position))
    open_positions = list(utilities.get_all_positions(scene.config) - coords)
    random.shuffle(open_positions)
    found = None
    while open_positions and not found:
        target = open_positions.pop()
        if roads.can_connect_to_road(scene, target):
            found = target
    return found


def _sleep(scene, brain: DefaultActiveActor, sleep_for: int) -> None:
    """# Adds the sleeping brain and a blinker animation."""
    brain._log_debug("falling asleep")
    from horderl.components.brains.sleeping_brain import SleepingBrain

    new_controller = SleepingBrain(
        entity=brain.entity, old_brain=brain.id, turns=sleep_for
    )
    blinker = BlinkerAnimationDefinition(
        entity=brain.entity,
        new_symbol="z",
        new_color=palettes.LIGHT_WATER,
        timer_delay=500,
    )
    scene.cm.stash_component(brain.id)
    scene.cm.add(new_controller, blinker)


def _attack_stationary_target(scene, brain: StationaryAttackActor) -> None:
    """# Stationary attacks use the same stab animation as default AI."""
    coords = scene.cm.get_one(Coordinates, entity=brain.entity)
    target = scene.cm.get_one(Coordinates, entity=brain.target)
    facing = coords.direction_towards(target)
    attack = scene.cm.get_one(Attack, entity=brain.entity)
    scene.cm.add(
        AttackAction(
            entity=brain.entity, target=brain.target, damage=attack.damage
        )
    )
    scene.cm.add(
        *stab(brain.entity, coords.x + facing[0], coords.y + facing[1])[1]
    )
    brain.pass_turn(get_current_turn(scene))


def _teleport_to_root(scene, brain: StationaryAttackActor) -> None:
    """# Teleporting directly mutates the coordinates component."""
    coords = scene.cm.get_one(Coordinates, entity=brain.entity)
    coords.x = brain.root_x
    coords.y = brain.root_y


def _farm(scene, brain: PeasantActor) -> None:
    """# Farming currently just consumes a turn."""
    brain.pass_turn(get_current_turn(scene))


def _wander(scene, brain: PeasantActor) -> None:
    """# Wandering prefers the lowest-cost adjacent tile."""
    cost_mapper = scene.cm.get_one(CostMapper, entity=brain.entity)
    if not cost_mapper:
        brain._log_debug("no cost mapper found")
        brain.intention = random.choice(STEPS)
        return

    step_costs = _get_possible_steps(scene, brain)

    if step_costs:
        random.shuffle(step_costs)
        step_costs = sorted(step_costs, key=lambda x: x[1])
        brain._log_debug(f"evaluated steps {step_costs}")
        brain.intention = step_costs[0][0]
    else:
        brain.pass_turn(get_current_turn(scene))


def _get_possible_steps(scene, brain: PeasantActor):
    """# Filters out steps outside map bounds."""
    cost_mapper = scene.cm.get_one(CostMapper, entity=brain.entity)
    cost_map = get_cost_map(scene, cost_mapper)
    coords = scene.cm.get_one(Coordinates, entity=brain.entity)
    step_costs = []
    for step in STEPS:
        if step not in [Intention.NONE, Intention.DALLY]:
            new_position = (
                STEP_VECTOR_MAP[step][0] + coords.position[0],
                STEP_VECTOR_MAP[step][1] + coords.position[1],
            )
            if (
                0 <= new_position[0] < scene.config.map_width
                and 0 <= new_position[1] < scene.config.map_height
            ):
                step_cost = (step, cost_map[new_position[0], new_position[1]])
                step_costs.append(step_cost)
    return step_costs


def _handle_player_input(scene, brain: PlayerBrain, action_map) -> None:
    """# Player input updates abilities, UI, and movement intentions."""
    key_event = core.get_key_event()
    if key_event:
        brain._log_debug(f"received input {key_event}")
        key_code = key_event.sym
        intention = action_map.get(key_code, None)
        brain._log_debug(f"translated {key_event} -> {intention}")

        tracker = scene.cm.get_one(AbilityTracker, entity=brain.entity)
        if intention == Intention.NEXT_ABILITY:
            ability_selection_system.increment(scene, tracker)
        elif intention == Intention.PREVIOUS_ABILITY:
            ability_selection_system.decrement(scene, tracker)
        elif intention == Intention.USE_ABILITY:
            ability = ability_selection_system.get_current_ability(
                scene, tracker
            )
            from horderl.systems.ability_system import apply_ability

            apply_ability(scene, brain.id, ability)
        elif intention == Intention.SHOW_HELP:
            scene.cm.add(ShowHelpDialogue(entity=brain.entity))
        elif intention == Intention.BACK:
            scene.cm.add(QuitGame(entity=brain.entity))
        elif intention is None:
            brain._log_debug("found no useable intention")
            return
        else:
            brain._log_debug(
                "deferred intention %s (usually for movement intentions)"
                % intention
            )
            brain.intention = intention


def _handle_dizzy_input(scene, brain: DizzyBrain, action_map) -> None:
    """# Dizzy input replaces movement with random steps."""
    key_event = core.get_key_event()
    if key_event:
        brain._log_debug(f"received input {key_event}")
        key_code = key_event.sym
        intention = action_map.get(key_code, None)
        brain._log_debug(f"translated {key_event} -> {intention}")

        tracker = scene.cm.get_one(AbilityTracker, entity=brain.entity)
        if intention == Intention.NEXT_ABILITY:
            ability_selection_system.increment(scene, tracker)
        elif intention == Intention.PREVIOUS_ABILITY:
            ability_selection_system.decrement(scene, tracker)
        elif intention == Intention.USE_ABILITY:
            ability = ability_selection_system.get_current_ability(
                scene, tracker
            )
            from horderl.systems.ability_system import apply_ability

            apply_ability(scene, brain.id, ability)
        elif intention == Intention.SHOW_HELP:
            scene.cm.add(ShowHelpDialogue(entity=brain.entity))
        elif intention is None:
            brain._log_debug("found no useable intention")
            return
        else:
            coords = scene.cm.get_one(Coordinates, entity=brain.entity)
            scene.cm.add(*confused_animation(coords.x, coords.y)[1])
            brain._log_debug(
                "deferred intention %s (usually for movement intentions)"
                % intention
            )
            brain._log_debug("taking a dizzy step")
            if brain.turns <= 1:
                from horderl.systems import brain_stack

                continuing_actor = brain_stack.back_out(scene, brain)
            else:
                continuing_actor = brain
            brain.turns -= 1
            continuing_actor.intention = random.choice(DIZZY_STEPS)


def _handle_fast_forward_input(
    scene, brain: FastForwardBrain, action_map
) -> None:
    """# Fast-forward input either delays or backs out."""
    key_event = core.get_key_event()
    if key_event:
        brain._log_debug(f"received input {key_event}")
        key_code = key_event.sym
        intention = action_map.get(key_code, None)
        brain._log_debug(f"translated {key_event} -> {intention}")
        if intention == Intention.BACK:
            from horderl.systems import brain_stack

            brain_stack.back_out(scene, brain)
            return
    else:
        brain.intention = Intention.DALLY


def _handle_player_dead_input(
    scene, brain: PlayerDeadBrain, action_map
) -> None:
    """# Player-dead input only allows ability selection."""
    key_event = core.get_key_event()
    if key_event:
        brain._log_debug(f"received input {key_event}")
        key_code = key_event.sym
        intention = action_map.get(key_code, None)
        brain._log_debug(f"translated {key_event} -> {intention}")

        tracker = scene.cm.get_one(AbilityTracker, entity=brain.entity)
        if intention is Intention.NEXT_ABILITY:
            ability_selection_system.increment(scene, tracker)
        elif intention is Intention.PREVIOUS_ABILITY:
            ability_selection_system.decrement(scene, tracker)
        elif intention is Intention.USE_ABILITY:
            ability = ability_selection_system.get_current_ability(
                scene, tracker
            )
            from horderl.systems.ability_system import apply_ability

            apply_ability(scene, brain.id, ability)
        elif intention is None:
            from horderl.i18n import t

            brain._log_debug("found no useable intention")
            scene.warn(t("warning.player_dead_no_action"))
            return


def _move_cursor(scene, brain, intention: Intention) -> None:
    """# Cursor moves are clamped to map bounds."""
    cursor_coords = scene.cm.get_one(Coordinates, entity=brain.cursor)
    direction = STEP_VECTORS[intention]
    cursor_coords.x += direction[0]
    cursor_coords.y += direction[1]
    if 0 > cursor_coords.x or cursor_coords.x >= scene.config.map_width:
        cursor_coords.x -= direction[0]
    if 0 > cursor_coords.y or cursor_coords.y >= scene.config.map_height:
        cursor_coords.y -= direction[1]


def _paint(scene, brain: PainterBrain) -> None:
    """# Painter brains delegate placement to the painter system."""
    painter_system.paint_at_cursor(scene, brain)


def _handle_look(scene, brain: LookCursorController) -> None:
    """# Look mode describes the top-priority entity under the cursor."""
    scene.message(_get_description(scene, brain))


def _get_description(scene, brain: LookCursorController) -> str:
    """# Prefer entity descriptions when available."""
    from engine.components.entity import Entity

    coords = scene.cm.get_one(Coordinates, entity=brain.cursor)
    viewables = scene.cm.get(
        Coordinates,
        query=lambda c: c.x == coords.x
        and c.y == coords.y
        and c.entity != brain.cursor,
    )
    viewables = sorted(viewables, key=lambda v: v.priority)
    if viewables:
        viewable = viewables[-1]
    else:
        return "grass"

    entity = scene.cm.get_one(Entity, entity=viewable.entity)
    if entity.description:
        return entity.description

    return entity.name


def _place_thing(scene, brain: PlaceThingActor, direction: Intention) -> None:
    """# Placement consumes gold and passes the turn."""
    coords = scene.cm.get_one(Coordinates, entity=brain.entity)
    direction = STEP_VECTORS[direction]
    thing_x = coords.x + direction[0]
    thing_y = coords.y + direction[1]
    if is_buildable(scene, thing_x, thing_y):
        placement_system.place(scene, brain, thing_x, thing_y)
        scene.gold -= brain.gold_cost
        from horderl.systems import brain_stack

        old_actor = brain_stack.back_out(scene, brain)
        old_actor.pass_turn(get_current_turn(scene))
    else:
        from horderl.systems import brain_stack

        brain_stack.back_out(scene, brain)


def is_buildable(scene, x: int, y: int) -> bool:
    """
    Report whether a tile can accept a new buildable.

    Args:
        scene: Active scene containing component manager.
        x: X coordinate to check.
        y: Y coordinate to check.

    Returns:
        bool: True if the tile is buildable.
    """
    target_coords = scene.cm.get(
        Coordinates,
        query=lambda coords: coords.x == x
        and coords.y == y
        and not coords.buildable,
    )
    return not target_coords


def _dig_hole(scene, brain: DigHoleActor, direction: Intention) -> None:
    """# Digging handles empty tiles and diggable objects."""
    coords = scene.cm.get_one(Coordinates, entity=brain.entity)
    direction = STEP_VECTORS[direction]
    hole_x = coords.x + direction[0]
    hole_y = coords.y + direction[1]
    if not _in_bounds(hole_x, hole_y, scene.config):
        scene.message(
            "You can't build outside of the town.", color=palettes.WHITE
        )
        from horderl.systems import brain_stack

        brain_stack.back_out(scene, brain)
    elif _is_empty(scene, hole_x, hole_y):
        _apply_dig_hole(hole_x, hole_y, scene, brain)
    else:
        diggable_entities = _get_diggables(scene, hole_x, hole_y)
        if diggable_entities:
            scene.gold -= 2
            entity = diggable_entities.pop()
            scene.cm.add(Die(entity=entity, killer=brain.entity))
            diggable = scene.cm.get_one(Diggable, entity=entity)
            if diggable.is_free:
                _apply_dig_hole(hole_x, hole_y, scene, brain)
                return
            else:
                from engine.components.entity import Entity

                entity_component = scene.cm.get_one(Entity, entity=entity)
                scene.message(f"You dug up {entity_component.name}.")

            dirt = make_dirt(hole_x, hole_y)
            scene.cm.add(*dirt[1])
            from horderl.systems import brain_stack

            old_actor = brain_stack.back_out(scene, brain)
            old_actor.pass_turn(get_current_turn(scene))
        else:
            from horderl.systems import brain_stack

            brain_stack.back_out(scene, brain)


def _apply_dig_hole(
    hole_x: int, hole_y: int, scene, brain: DigHoleActor
) -> None:
    """# Applying a dig hole always spends gold and a turn."""
    scene.message("You dug a deep hole.")
    hole = make_hole(hole_x, hole_y)
    scene.cm.add(*hole[1])
    scene.gold -= 2
    from horderl.systems import brain_stack

    old_actor = brain_stack.back_out(scene, brain)
    old_actor.pass_turn(get_current_turn(scene))


def _in_bounds(x: int, y: int, config) -> bool:
    """# Bounds check is inclusive of map edges."""
    in_x_bounds = 0 <= x <= config.map_width - 1
    in_y_bounds = 0 <= y <= config.map_height - 1
    return in_y_bounds and in_x_bounds


def _is_empty(scene, x: int, y: int) -> bool:
    """# Empty tiles have no blocking coordinates."""
    target_coords = scene.cm.get(
        Coordinates,
        query=lambda coords: coords.x == x
        and coords.y == y
        and not coords.buildable,
    )
    return not target_coords


def _get_diggables(scene, x: int, y: int) -> List[int]:
    """# Diggable entities are sorted by priority before returning."""
    fillable_entities = scene.cm.get(
        Coordinates,
        query=lambda coords: coords.x == x
        and coords.y == y
        and scene.cm.get_one(Diggable, entity=coords.entity),
    )
    return [
        fe.entity
        for fe in sorted(fillable_entities, key=lambda fe: fe.priority)
    ]


def _shoot(scene, brain: RangedAttackActor) -> None:
    """# Shooting consumes an ability use and exits ranged mode."""
    attack = AttackAction(entity=brain.entity, target=brain.target, damage=1)
    scene.cm.add(attack)

    ability = scene.cm.get_component_by_id(brain.shoot_ability)
    ability.count -= 1

    _exit_ranged_attack(scene, brain)


def _exit_ranged_attack(scene, brain: RangedAttackActor) -> None:
    """# Clears target highlighting before backing out."""
    blinker = scene.cm.get_one(BlinkerAnimationDefinition, entity=brain.target)
    if blinker:
        blinker.is_animating = False
        blinker.remove_on_stop = True
    from horderl.systems import brain_stack

    brain_stack.back_out(scene, brain)


def _next_enemy(scene, brain: RangedAttackActor) -> None:
    """# Cycling enemies updates the blinker target."""
    next_enemy = _get_next_enemy(scene, brain)
    old_blinker = scene.cm.get_one(
        BlinkerAnimationDefinition, entity=brain.target
    )
    if old_blinker:
        old_blinker.is_animating = False
        old_blinker.remove_on_stop = True
    scene.cm.add(BlinkerAnimationDefinition(entity=next_enemy))
    brain.target = next_enemy


def _get_next_enemy(scene, brain: RangedAttackActor) -> int:
    """# Enemy cycling is based on visible hordeling IDs."""
    current_target = next(
        (
            tag
            for tag in scene.cm.get_all(Tag, entity=brain.target)
            if tag.tag_type == TagType.HORDELING
        ),
        None,
    )
    all_enemies = scene.cm.get(
        Tag, query=lambda tag: tag.tag_type == TagType.HORDELING
    )
    visible_enemies = [
        e
        for e in all_enemies
        if is_visible(scene, scene.cm.get_one(Coordinates, entity=e.entity))
    ]
    enemies = sorted(visible_enemies, key=lambda x: x.id)

    index = enemies.index(current_target)
    next_index = (index + 1) % len(enemies)
    return enemies[next_index].entity


def _sell_thing(scene, brain: SellThingActor, direction: Intention) -> None:
    """# Selling destroys the entity and replaces it with dirt."""
    coords = scene.cm.get_one(Coordinates, entity=brain.entity)
    direction = STEP_VECTORS[direction]
    hole_x = coords.x + direction[0]
    hole_y = coords.y + direction[1]
    sellables = _get_sellables(scene, (hole_x, hole_y))
    if sellables:
        assert len(sellables) == 1, "found more than one sellable on a tile"
        entity = sellables.pop()
        scene.cm.add(Die(entity=entity, killer=brain.entity))
        sellable: Sellable = scene.cm.get_one(Sellable, entity=entity)
        from engine.components.entity import Entity

        entity_component = scene.cm.get_one(Entity, entity=entity)
        if not entity_component:
            brain._log_warning(f"found a sellable without an entity: {entity}")
        scene.message(
            f"You sold a {entity_component.name} for {sellable.value}c!",
            color=palettes.GOLD,
        )

        scene.gold += sellable.value
        dirt = make_dirt(hole_x, hole_y)
        scene.cm.add(*dirt[1])
        from horderl.systems import brain_stack

        old_actor = brain_stack.back_out(scene, brain)
        old_actor.pass_turn(get_current_turn(scene))
    else:
        from horderl.systems import brain_stack

        brain_stack.back_out(scene, brain)


def _get_sellables(scene, point) -> List[int]:
    """# Sellable entities are filtered by matching coordinates."""
    sellables = set(scene.cm.get(Sellable, project=lambda s: s.entity))
    nearby = [
        c.entity
        for c in scene.cm.get(Coordinates)
        if c.distance_from_point(point[0], point[1]) == 0
        and c.entity in sellables
    ]
    return nearby


def _handle_sleeping_back_out(scene, brain: SleepingBrain) -> None:
    """# Sleep cleanup processes any digested peasant."""
    stomach = scene.cm.get_one(Stomach, entity=brain.entity)
    if stomach:
        if stomach.contents != constants.INVALID:
            brain._log_debug("digested the peasant")
            scene.warn("A peasant has been lost!")
            scene.cm.add(PeasantDied(entity=core.get_id("world")))
        clear_stomach(scene, stomach)


DIZZY_STEPS = [
    Intention.STEP_NORTH,
    Intention.STEP_SOUTH,
    Intention.STEP_EAST,
    Intention.STEP_WEST,
]

PLAYER_KEY_ACTION_MAP = {
    tcod.event.KeySym.e: Intention.NEXT_ABILITY,
    tcod.event.KeySym.q: Intention.PREVIOUS_ABILITY,
    tcod.event.KeySym.SPACE: Intention.USE_ABILITY,
    tcod.event.KeySym.h: Intention.SHOW_HELP,
    tcod.event.KeySym.UP: Intention.STEP_NORTH,
    tcod.event.KeySym.DOWN: Intention.STEP_SOUTH,
    tcod.event.KeySym.RIGHT: Intention.STEP_EAST,
    tcod.event.KeySym.LEFT: Intention.STEP_WEST,
    tcod.event.KeySym.PERIOD: Intention.DALLY,
    tcod.event.KeySym.ESCAPE: Intention.BACK,
}

DIZZY_KEY_ACTION_MAP = {
    tcod.event.KeySym.e: Intention.NEXT_ABILITY,
    tcod.event.KeySym.q: Intention.PREVIOUS_ABILITY,
    tcod.event.KeySym.SPACE: Intention.USE_ABILITY,
    tcod.event.KeySym.h: Intention.SHOW_HELP,
    tcod.event.KeySym.UP: Intention.STEP_NORTH,
    tcod.event.KeySym.DOWN: Intention.STEP_SOUTH,
    tcod.event.KeySym.RIGHT: Intention.STEP_EAST,
    tcod.event.KeySym.LEFT: Intention.STEP_WEST,
    tcod.event.KeySym.PERIOD: Intention.DALLY,
    tcod.event.KeySym.ESCAPE: Intention.BACK,
}

FAST_FORWARD_KEY_ACTION_MAP = {
    tcod.event.KeySym.PERIOD: Intention.DALLY,
    tcod.event.KeySym.ESCAPE: Intention.BACK,
}

PLAYER_DEAD_KEY_ACTION_MAP = {
    tcod.event.KeySym.e: Intention.NEXT_ABILITY,
    tcod.event.KeySym.q: Intention.PREVIOUS_ABILITY,
    tcod.event.KeySym.SPACE: Intention.USE_ABILITY,
    tcod.event.KeySym.ESCAPE: Intention.BACK,
}

PAINTER_KEY_ACTION_MAP = {
    tcod.event.KeySym.UP: Intention.STEP_NORTH,
    tcod.event.KeySym.DOWN: Intention.STEP_SOUTH,
    tcod.event.KeySym.RIGHT: Intention.STEP_EAST,
    tcod.event.KeySym.LEFT: Intention.STEP_WEST,
    tcod.event.KeySym.ESCAPE: Intention.BACK,
    tcod.event.KeySym.SPACE: Intention.USE_ABILITY,
}

LOOK_CURSOR_KEY_ACTION_MAP = {
    tcod.event.KeySym.UP: Intention.STEP_NORTH,
    tcod.event.KeySym.DOWN: Intention.STEP_SOUTH,
    tcod.event.KeySym.RIGHT: Intention.STEP_EAST,
    tcod.event.KeySym.LEFT: Intention.STEP_WEST,
    tcod.event.KeySym.ESCAPE: Intention.BACK,
    tcod.event.KeySym.SPACE: Intention.USE_ABILITY,
}

PLACE_THING_KEY_ACTION_MAP = {
    tcod.event.KeySym.UP: Intention.STEP_NORTH,
    tcod.event.KeySym.DOWN: Intention.STEP_SOUTH,
    tcod.event.KeySym.RIGHT: Intention.STEP_EAST,
    tcod.event.KeySym.LEFT: Intention.STEP_WEST,
    tcod.event.KeySym.ESCAPE: Intention.BACK,
}

DIG_HOLE_KEY_ACTION_MAP = {
    tcod.event.KeySym.UP: Intention.STEP_NORTH,
    tcod.event.KeySym.DOWN: Intention.STEP_SOUTH,
    tcod.event.KeySym.RIGHT: Intention.STEP_EAST,
    tcod.event.KeySym.LEFT: Intention.STEP_WEST,
    tcod.event.KeySym.ESCAPE: Intention.BACK,
}

RANGED_ATTACK_KEY_ACTION_MAP = {
    tcod.event.KeySym.SPACE: Intention.USE_ABILITY,
    tcod.event.KeySym.UP: Intention.STEP_NORTH,
    tcod.event.KeySym.DOWN: Intention.STEP_SOUTH,
    tcod.event.KeySym.RIGHT: Intention.STEP_EAST,
    tcod.event.KeySym.LEFT: Intention.STEP_WEST,
    tcod.event.KeySym.ESCAPE: Intention.BACK,
}

SELL_THING_KEY_ACTION_MAP = {
    tcod.event.KeySym.UP: Intention.STEP_NORTH,
    tcod.event.KeySym.DOWN: Intention.STEP_SOUTH,
    tcod.event.KeySym.RIGHT: Intention.STEP_EAST,
    tcod.event.KeySym.LEFT: Intention.STEP_WEST,
    tcod.event.KeySym.ESCAPE: Intention.BACK,
}

STEP_VECTORS = {
    Intention.STEP_NORTH: (0, -1),
    Intention.STEP_SOUTH: (0, 1),
    Intention.STEP_EAST: (1, 0),
    Intention.STEP_WEST: (-1, 0),
    Intention.STEP_NORTH_EAST: (1, -1),
    Intention.STEP_NORTH_WEST: (-1, -1),
    Intention.STEP_SOUTH_EAST: (1, 1),
    Intention.STEP_SOUTH_WEST: (-1, 1),
}
