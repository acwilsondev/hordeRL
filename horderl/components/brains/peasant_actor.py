import random
from dataclasses import dataclass
from enum import Enum

from engine.components import Coordinates, EnergyActor
from engine.logging import get_logger
from horderl.components.actors import STEP_VECTOR_MAP, STEPS
from horderl.components.brains.brain import Brain
from horderl.components.enums import Intention
from horderl.components.pathfinding.cost_mapper import CostMapper


@dataclass
class PeasantActor(Brain):
    """
    Brain controlling peasant movement and idle behavior.

    Responsible for deciding between farming, wandering, or idling based on
    internal state and available pathing information.
    """

    class State(str, Enum):
        """
        Possible behavior modes for the peasant brain.
        """

        UNKNOWN = "UNKNOWN"
        FARMING = "FARMING"
        HIDING = "HIDING"
        WANDERING = "WANDERING"

    state: State = State.UNKNOWN
    can_animate: bool = True
    energy_cost: int = EnergyActor.HOURLY

    def act(self, scene):
        """
        Execute one behavioral tick based on the peasant state.

        Args:
            scene: Active scene containing component manager and config.

        Side Effects:
            - Updates intention or consumes energy via pass_turn().
        """
        logger = get_logger(__name__)
        logger.debug(
            "Peasant actor tick",
            extra={"entity": self.entity, "state": self.state.value},
        )
        if self.state is PeasantActor.State.FARMING:
            self.farm(scene)
        elif self.state is PeasantActor.State.WANDERING:
            self.wander(scene)
        else:
            self.pass_turn()

    def farm(self, scene):
        """
        Spend a turn farming (currently a no-op).

        Args:
            scene: Active scene containing component manager.

        Side Effects:
            - Consumes energy via pass_turn().
        """
        self.pass_turn()

    def wander(self, scene):
        """
        Choose a low-cost adjacent step or idle if no path is available.

        Args:
            scene: Active scene containing component manager and config.

        Side Effects:
            - Updates intention when a step is chosen.
            - Consumes energy via pass_turn() when no step is found.
        """
        cost_mapper = scene.cm.get_one(CostMapper, entity=self.entity)
        if not cost_mapper:
            self._log_debug("no cost mapper found")
            self.intention = random.choice(STEPS)
            return

        step_costs = self.get_possible_steps(scene)

        if step_costs:
            # shuffle to perturb the stable sort
            random.shuffle(step_costs)
            step_costs = sorted(step_costs, key=lambda x: x[1])
            self._log_debug(f"evaluated steps {step_costs}")
            self.intention = step_costs[0][0]
        else:
            # nowhere to go
            self.pass_turn()

    def get_possible_steps(self, scene):
        """
        Gather valid step intentions with associated costs.

        Args:
            scene: Active scene containing component manager and config.

        Returns:
            list[tuple]: List of (intention, cost) tuples.
        """
        cost_mapper = scene.cm.get_one(CostMapper, entity=self.entity)
        cost_map = cost_mapper.get_cost_map(scene)
        coords = scene.cm.get_one(Coordinates, entity=self.entity)
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
                    step_cost = (
                        step,
                        cost_map[new_position[0], new_position[1]],
                    )
                    step_costs.append(step_cost)
        return step_costs
