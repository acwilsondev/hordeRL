import random
from typing import Callable, Optional

from engine import core
from engine.components import Actor, Coordinates
from engine.logging import get_logger
from horderl.components import Appearance
from horderl.components.animation_definitions import (
    BlinkerAnimationDefinition,
    FloatAnimationDefinition,
    PathAnimationDefinition,
    RandomizedBlinkerAnimationDefinition,
    ResetOwnerAnimationDefinition,
    SequenceAnimationDefinition,
)
from horderl.components.events.delete_event import Delete
from horderl.components.path_node import PathNode
from horderl.components.relationships.owner import Owner
from horderl.systems.rendering.appearance_helpers import update_appearance

logger = get_logger(__name__)


def run(scene, dt_ms: int) -> None:
    """
    Run all animation controller systems for the current update tick.

    Args:
        scene: The active game scene.
        dt_ms: Time elapsed since the last update, in milliseconds.

    Side effects:
        - Updates animation component state.
        - Mutates entity appearance, coordinates, and lifecycle.
    """
    _run_blinker(scene, dt_ms)
    _run_randomized_blinker(scene, dt_ms)
    _run_float(scene, dt_ms)
    _run_path(scene, dt_ms)
    _run_sequence(scene, dt_ms)
    _run_reset_owner(scene)


def _process_timed_animation(
    scene,
    animation,
    on_start: Callable,
    on_step: Callable,
    on_stop: Callable,
) -> None:
    # Ensure stop cleanup happens even if another system halted the animation.
    if not animation.is_animating:
        _process_stop(scene, animation, on_stop)
        return

    now = core.time_ms()
    if animation.next_update > now:
        return

    if not animation.started:
        on_start(scene, animation)
        animation.started = True

    animation.next_update = now + animation.timer_delay
    on_step(scene, animation)


def _process_stop(scene, animation, on_stop: Callable) -> None:
    if animation.stop_processed:
        return

    on_stop(scene, animation)
    animation.stop_processed = True

    if animation.delete_on_complete:
        scene.cm.delete(animation.entity)
        return

    if animation.remove_on_stop:
        scene.cm.delete_component(animation)


def _stop_animation(scene, animation, on_stop: Callable) -> None:
    animation.is_animating = False
    _process_stop(scene, animation, on_stop)


def _get_appearance(scene, entity, error_message: str) -> Optional[Appearance]:
    appearance = scene.cm.get_one(Appearance, entity=entity)
    if not appearance:
        logger.error(error_message, extra={"entity": entity})
    return appearance


def _run_blinker(scene, dt_ms: int) -> None:
    def on_start(scene, animation: BlinkerAnimationDefinition) -> None:
        appearance = _get_appearance(
            scene,
            animation.entity,
            "BlinkerAnimationDefinition requires an Appearance component",
        )
        if not appearance:
            animation.is_animating = False
            return
        animation.original_symbol = appearance.symbol
        animation.original_color = appearance.color
        animation.original_bg_color = appearance.bg_color

    def on_step(scene, animation: BlinkerAnimationDefinition) -> None:
        appearance = _get_appearance(
            scene,
            animation.entity,
            "BlinkerAnimationDefinition missing Appearance during update",
        )
        if not appearance:
            _stop_animation(scene, animation, on_stop)
            return
        if animation.is_on:
            update_appearance(
                appearance,
                animation.new_symbol,
                animation.new_color,
                animation.new_bg_color,
            )
        else:
            update_appearance(
                appearance,
                animation.original_symbol,
                animation.original_color,
                animation.original_bg_color,
            )
        animation.is_on = not animation.is_on

    def on_stop(scene, animation: BlinkerAnimationDefinition) -> None:
        appearance = _get_appearance(
            scene,
            animation.entity,
            "BlinkerAnimationDefinition missing Appearance during stop",
        )
        if not appearance:
            return
        if animation.original_symbol is None:
            return
        update_appearance(
            appearance,
            animation.original_symbol,
            animation.original_color,
            animation.original_bg_color,
        )

    for animation in scene.cm.get(BlinkerAnimationDefinition):
        _process_timed_animation(scene, animation, on_start, on_step, on_stop)


def _run_randomized_blinker(scene, dt_ms: int) -> None:
    def on_start(
        scene, animation: RandomizedBlinkerAnimationDefinition
    ) -> None:
        appearance = _get_appearance(
            scene,
            animation.entity,
            "RandomizedBlinkerAnimationDefinition requires an Appearance component",
        )
        if not appearance:
            raise ValueError(
                "RandomizedBlinkerAnimationDefinition requires an Appearance component"
            )
        animation.original_symbol = appearance.symbol
        animation.original_color = appearance.color
        animation.original_bg_color = appearance.bg_color

    def on_step(
        scene, animation: RandomizedBlinkerAnimationDefinition
    ) -> None:
        appearance = _get_appearance(
            scene,
            animation.entity,
            "RandomizedBlinkerAnimationDefinition missing Appearance during update",
        )
        if not appearance:
            _stop_animation(scene, animation, on_stop)
            return
        if animation.is_on:
            update_appearance(
                appearance,
                animation.new_symbol,
                animation.new_color,
                animation.new_bg_color,
            )
        else:
            update_appearance(
                appearance,
                animation.original_symbol,
                animation.original_color,
                animation.original_bg_color,
            )
        animation.is_on = not animation.is_on
        animation.timer_delay = random.randint(
            animation.min_timer_delay,
            animation.max_timer_delay,
        )

    def on_stop(
        scene, animation: RandomizedBlinkerAnimationDefinition
    ) -> None:
        appearance = _get_appearance(
            scene,
            animation.entity,
            "RandomizedBlinkerAnimationDefinition missing Appearance during stop",
        )
        if not appearance:
            return
        if animation.original_symbol is None:
            return
        update_appearance(
            appearance,
            animation.original_symbol,
            animation.original_color,
            animation.original_bg_color,
        )

    for animation in scene.cm.get(RandomizedBlinkerAnimationDefinition):
        _process_timed_animation(scene, animation, on_start, on_step, on_stop)


def _run_float(scene, dt_ms: int) -> None:
    def on_start(scene, animation: FloatAnimationDefinition) -> None:
        coordinates = scene.cm.get_one(Coordinates, entity=animation.entity)
        if not coordinates:
            animation.is_animating = False

    def on_step(scene, animation: FloatAnimationDefinition) -> None:
        coordinates = scene.cm.get_one(Coordinates, entity=animation.entity)
        if not coordinates:
            _stop_animation(scene, animation, on_stop)
            return

        up_or_over = random.choice([(0, -1), (1, 0)])
        coordinates.x += up_or_over[0]
        coordinates.y += up_or_over[1]

        if coordinates.x >= scene.config.map_width or coordinates.y <= 0:
            _stop_animation(scene, animation, on_stop)
            return

        animation.duration -= 1
        if animation.duration < 0:
            _stop_animation(scene, animation, on_stop)

    def on_stop(scene, animation: FloatAnimationDefinition) -> None:
        return

    for animation in scene.cm.get(FloatAnimationDefinition):
        _process_timed_animation(scene, animation, on_start, on_step, on_stop)


def _run_path(scene, dt_ms: int) -> None:
    def on_start(scene, animation: PathAnimationDefinition) -> None:
        coordinates = scene.cm.get_one(Coordinates, entity=animation.entity)
        if not coordinates:
            animation.is_animating = False

    def on_step(scene, animation: PathAnimationDefinition) -> None:
        coordinates = scene.cm.get_one(Coordinates, entity=animation.entity)
        if not coordinates:
            _stop_animation(scene, animation, on_stop)
            return

        path_nodes = scene.cm.get_all(PathNode, entity=animation.entity)
        try:
            next_node = next(
                node
                for node in path_nodes
                if node.step == animation.current_step
            )
        except StopIteration:
            _stop_animation(scene, animation, on_stop)
            return

        coordinates.x = next_node.x
        coordinates.y = next_node.y
        animation.current_step += 1

    def on_stop(scene, animation: PathAnimationDefinition) -> None:
        return

    for animation in scene.cm.get(PathAnimationDefinition):
        _process_timed_animation(scene, animation, on_start, on_step, on_stop)


def _run_sequence(scene, dt_ms: int) -> None:
    def on_start(scene, animation: SequenceAnimationDefinition) -> None:
        appearance = scene.cm.get_one(Appearance, entity=animation.entity)
        if not appearance:
            animation.is_animating = False

    def on_step(scene, animation: SequenceAnimationDefinition) -> None:
        if animation.current_step >= len(animation.sequence):
            _stop_animation(scene, animation, on_stop)
            return

        appearance = scene.cm.get_one(Appearance, entity=animation.entity)
        if not appearance:
            _stop_animation(scene, animation, on_stop)
            return

        color, symbol = animation.sequence[animation.current_step]
        appearance.symbol = symbol
        appearance.color = color
        animation.current_step += 1

    def on_stop(scene, animation: SequenceAnimationDefinition) -> None:
        return

    for animation in scene.cm.get(SequenceAnimationDefinition):
        _process_timed_animation(scene, animation, on_start, on_step, on_stop)


def _run_reset_owner(scene) -> None:
    for reset in scene.cm.get(ResetOwnerAnimationDefinition):
        delete_event = scene.cm.get_one(Delete, entity=reset.entity)
        if not delete_event:
            continue

        owner = scene.cm.get_one(Owner, entity=reset.entity)
        if not owner:
            continue

        peasant = scene.cm.get_one(Actor, entity=owner.owner)
        if not peasant:
            continue

        peasant.can_animate = True
