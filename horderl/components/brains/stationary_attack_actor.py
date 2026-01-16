from dataclasses import dataclass

from engine import constants
from engine.components import Coordinates
from engine.logging import get_logger
from horderl.components.actions.attack_action import AttackAction
from horderl.components.attacks.attack import Attack
from horderl.components.brains.brain import Brain
from horderl.components.events.attack_started_events import AttackStartListener
from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)
from horderl.components.tags.hordeling_tag import HordelingTag
from horderl.content.attacks import stab


@dataclass
class StationaryAttackActor(Brain, SeasonResetListener, AttackStartListener):
    """
    Stand in place and attack any enemy in range.
    """

    target: int = constants.INVALID
    cost_map = None
    root_x: int = constants.INVALID
    root_y: int = constants.INVALID

    def on_season_reset(self, scene, season):
        """
        Reset position to root at the start of a season.

        Args:
            scene: Active scene containing component manager.
            season: Season value triggering the reset.

        Side Effects:
            - Teleports the actor back to its root coordinates.
        """
        self.teleport_to_root(scene)

    def on_attack_start(self, scene):
        """
        Reset position to root when an attack sequence begins.

        Args:
            scene: Active scene containing component manager.

        Side Effects:
            - Teleports the actor back to its root coordinates.
        """
        self.teleport_to_root(scene)

    def teleport_to_root(self, scene):
        """
        Move the actor back to its root coordinates.

        Args:
            scene: Active scene containing component manager.

        Side Effects:
            - Mutates the Coordinates component for this entity.
        """
        coords = scene.cm.get_one(Coordinates, entity=self.entity)
        coords.x = self.root_x
        coords.y = self.root_y

    def act(self, scene):
        """
        Select and attack a nearby target, if any exist.

        Args:
            scene: Active scene containing component manager.

        Side Effects:
            - Updates target selection.
            - Adds attack actions/animations.
            - Consumes energy via pass_turn().
        """
        logger = get_logger(__name__)
        logger.debug(
            "Stationary attacker tick",
            extra={"entity": self.entity, "root": (self.root_x, self.root_y)},
        )
        coords = scene.cm.get_one(Coordinates, entity=self.entity)
        targets = scene.cm.get(
            Coordinates,
            query=lambda c: scene.cm.get_one(HordelingTag, entity=c.entity)
            and c.distance_from(coords) <= 2,
            project=lambda c: c.entity,
        )
        if not targets:
            self.pass_turn()
            return
        self.target = targets.pop()
        self.attack_target(scene)

    def attack_target(self, scene):
        """
        Execute an attack against the current target.

        Args:
            scene: Active scene containing component manager.

        Side Effects:
            - Adds attack actions and animation components.
            - Consumes energy via pass_turn().
        """
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
            bool: True if the target is close enough to attack.
        """
        coords = scene.cm.get_one(Coordinates, entity=self.entity)
        target = scene.cm.get_one(Coordinates, entity=self.target)
        return coords.distance_from(target) < 2
