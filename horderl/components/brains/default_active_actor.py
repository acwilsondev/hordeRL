import random
from dataclasses import dataclass
from typing import Optional

from engine import constants, utilities
from engine.components import Coordinates
from engine.logging import get_logger
from horderl import palettes
from horderl.components.actions.attack_action import AttackAction
from horderl.components.actions.eat_action import EatAction
from horderl.components.actions.tunnel_to_point import TunnelToPoint
from horderl.components.actors import VECTOR_STEP_MAP
from horderl.components.animation_definitions.blinker_animation_definition import (
    BlinkerAnimationDefinition,
)
from horderl.components.attacks.attack import Attack
from horderl.components.brains.brain import Brain
from horderl.components.brains.sleeping_brain import SleepingBrain
from horderl.components.edible import Edible
from horderl.components.events.die_events import Die
from horderl.components.pathfinding.breadcrumb_tracker import BreadcrumbTracker
from horderl.components.pathfinding.cost_mapper import CostMapper
from horderl.components.pathfinding.normal_cost_mapper import NormalCostMapper
from horderl.components.pathfinding.pathfinder import Pathfinder
from horderl.components.pathfinding.target_evaluation.hordeling_target_evaluator import (
    HordelingTargetEvaluator,
)
from horderl.components.pathfinding.target_evaluation.target_evaluator import (
    TargetEvaluator,
)
from horderl.content.attacks import stab
from horderl.content.terrain import roads
from horderl.systems.pathfinding.target_selection import get_new_target


@dataclass
class DefaultActiveActor(Brain):
    """
    Brain that selects and pursues targets for active hostile actors.

    Responsible for acquiring a target, deciding whether to eat or attack, and
    moving toward the target using pathfinding or emergency tunneling.
    """

    target: int = constants.INVALID
    cost_map = None

    def act(self, scene):
        """
        Evaluate targets and perform a single action toward the best option.

        Args:
            scene: Active scene containing component manager and config.

        Side Effects:
            - Updates internal target state and intention.
            - Enqueues actions or movement components.
            - Consumes energy via pass_turn().
        """
        logger = get_logger(__name__)
        logger.debug(
            "Default active actor tick",
            extra={"entity": self.entity, "target": self.target},
        )
        self.cost_map = self.get_cost_map(scene)

        target_evaluator = scene.cm.get_one(
            TargetEvaluator, entity=self.entity
        )
        if not target_evaluator:
            self._log_warning("missing target evaluator")
            target_evaluator = HordelingTargetEvaluator()

        entity_values = target_evaluator.get_targets(scene)

        if not entity_values:
            # No targets
            self.pass_turn()
            return

        coords = scene.cm.get_one(Coordinates, entity=self.entity)
        self.target = get_new_target(
            scene, self.cost_map, (coords.x, coords.y), entity_values
        )

        if self.is_target_in_range(scene):
            if self.should_eat(scene):
                self.eat_target(scene)
            else:
                self.attack_target(scene)
        else:
            self.move_towards_target(scene)

    def get_cost_map(self, scene):
        """
        Determine the cost map used for pathfinding.

        Args:
            scene: Active scene containing component manager.

        Returns:
            Any: Pathfinding cost map produced by a cost mapper.
        """
        cost_mapper: Optional[CostMapper] = scene.cm.get_one(
            CostMapper, entity=self.entity
        )
        if cost_mapper:
            return cost_mapper.get_cost_map(scene)
        else:
            # If one hasn't been set up, we default to the normal behavior
            return NormalCostMapper(entity=self.entity).get_cost_map(scene)

    def move_towards_target(self, scene):
        """
        Move toward the current target or tunnel if no path exists.

        Args:
            scene: Active scene containing component manager and config.

        Side Effects:
            - Sets the actor intention for the next step.
            - Adds tunneling actions or death events when blocked.
            - Consumes energy via pass_turn().
        """
        self._log_debug(f"stepping towards target {self.target}")
        coords = scene.cm.get_one(Coordinates, entity=self.entity)
        next_step_node = self.get_next_step(scene)
        if next_step_node is None:
            self._log_debug("can't find a natural path")
            tunnel_target = self._get_emergency_step(scene)
            if tunnel_target:
                scene.cm.add(
                    TunnelToPoint(entity=self.entity, point=tunnel_target)
                )
            else:
                self._log_warning("can't find a safe place to tunnel to")
                scene.cm.add(Die(entity=self.entity))
            self.pass_turn()
        else:
            next_step = (
                next_step_node[0] - coords.x,
                next_step_node[1] - coords.y,
            )
            self.intention = VECTOR_STEP_MAP[next_step]
            self._log_debug(f"set intention {self.intention}")

    def should_eat(self, scene):
        """
        Decide whether the current target is edible.

        Args:
            scene: Active scene containing component manager.

        Returns:
            bool: True if the target has an Edible component.
        """
        self._log_debug(f"checking for edibility of {self.target}")
        edible = scene.cm.get_one(Edible, entity=self.target)
        return edible is not None

    def eat_target(self, scene):
        """
        Trigger an eat action against the current target.

        Args:
            scene: Active scene containing component manager.

        Side Effects:
            - Adds an EatAction component.
            - Transitions the actor into a sleeping brain state.
            - Consumes energy via pass_turn().
        """
        self._log_debug(f"eating target {self.target}")
        scene.cm.add(EatAction(entity=self.entity, target=self.target))
        edible = scene.cm.get_one(Edible, entity=self.target)

        self.sleep(scene, edible.sleep_for)
        self.pass_turn()

    def attack_target(self, scene):
        """
        Trigger an attack action against the current target.

        Args:
            scene: Active scene containing component manager.

        Side Effects:
            - Adds AttackAction and animation components.
            - Consumes energy via pass_turn().
        """
        self._log_debug(f"attacking target {self.target}")

        coords = scene.cm.get_one(Coordinates, entity=self.entity)
        target = scene.cm.get_one(Coordinates, entity=self.target)
        facing = coords.direction_towards(target)
        attack = scene.cm.get_one(Attack, entity=self.entity)
        scene.cm.add(
            AttackAction(
                entity=self.entity, target=self.target, damage=attack.damage
            )
        )
        scene.cm.add(
            *stab(self.entity, coords.x + facing[0], coords.y + facing[1])[1]
        )
        self.pass_turn()

    def is_target_in_range(self, scene) -> bool:
        """
        Check whether the target is within attack range.

        Args:
            scene: Active scene containing component manager.

        Returns:
            bool: True if the target is close enough to interact.
        """
        coords = scene.cm.get_one(Coordinates, entity=self.entity)
        target = scene.cm.get_one(Coordinates, entity=self.target)
        return coords.distance_from(target) < 2

    def get_next_step(self, scene):
        """
        Calculate the next step on the path toward the target.

        Args:
            scene: Active scene containing component manager.

        Returns:
            tuple | None: Next path node coordinates, or None if no path exists.

        Side Effects:
            - Adds breadcrumb tracking components when available.
        """
        self_coords = scene.cm.get_one(Coordinates, entity=self.entity)
        target_coords = scene.cm.get_one(Coordinates, entity=self.target)
        path = Pathfinder().get_path(
            self.cost_map, self_coords.position, target_coords.position
        )

        breadcrumb_tracker = scene.cm.get_one(
            BreadcrumbTracker, entity=self.entity
        )
        if breadcrumb_tracker:
            breadcrumb_tracker.add_breadcrumbs(scene, path)

        path = [p for p in path]

        if len(path) <= 1:
            return None
        return path[1]

    def _get_emergency_step(self, scene):
        """
        Search for a point to tunnel to.
        """
        self._log_debug("searching for emergency step for tunnel")

        coords = set(scene.cm.get(Coordinates, project=lambda c: c.position))
        open_positions = list(
            utilities.get_all_positions(scene.config) - coords
        )
        random.shuffle(open_positions)
        found = None
        while open_positions and not found:
            target = open_positions.pop()
            if roads.can_connect_to_road(scene, target):
                found = target
        return found

    def sleep(self, scene, sleep_for):
        """
        Transition this actor into a sleeping brain state.

        Args:
            scene: Active scene containing component manager.
            sleep_for (int): Number of turns to sleep.

        Side Effects:
            - Stashes the current brain component.
            - Adds a SleepingBrain and blinker animation.
        """
        self._log_debug("falling asleep")
        new_controller = SleepingBrain(
            entity=self.entity, old_brain=self.id, turns=sleep_for
        )
        blinker = BlinkerAnimationDefinition(
            entity=self.entity,
            new_symbol="z",
            new_color=palettes.LIGHT_WATER,
            timer_delay=500,
        )
        scene.cm.stash_component(self.id)
        scene.cm.add(new_controller, blinker)
