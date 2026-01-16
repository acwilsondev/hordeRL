from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable

from engine.logging import get_logger

from ..abilities.ability import Ability
from ..animation_definitions.blinker_animation_definition import (
    BlinkerAnimationDefinition,
)


@dataclass
class ControlModeAbility(Ability, ABC):
    """
    Ability that swaps the controlling brain and animates the transition.

    This base class coordinates swapping the current brain/controller with a
    new mode while adding a blinker animation to visually indicate the change.
    """

    def use(self, scene, dispatcher):
        """
        Swap the active controller for the entity and add a blinker animation.

        Args:
            scene: Active scene providing access to the component manager.
            dispatcher: The current brain/controller being replaced.

        Side Effects:
            - Stashes the dispatcher component.
            - Adds a new controller and blinker animation to the entity.
        """
        logger = get_logger(__name__)
        logger.debug(
            "Switching control mode",
            extra={
                "entity": self.entity,
                "ability": type(self).__name__,
                "dispatcher": type(dispatcher).__name__,
            },
        )
        sym, color = self.get_anim()
        mode = self.get_mode()
        new_controller = mode(entity=self.entity, old_brain=dispatcher)
        blinker = BlinkerAnimationDefinition(
            entity=self.entity, new_symbol=sym, new_color=color
        )
        scene.cm.stash_component(dispatcher)
        scene.cm.add(new_controller, blinker)

    @abstractmethod
    def get_mode(self) -> Callable:
        """
        Provide the controller/brain class to activate for this ability.

        Returns:
            Callable: A callable/class that builds the new controller.
        """
        pass

    @abstractmethod
    def get_anim(self):
        """
        Provide the animation symbol and color for the mode change.

        Returns:
            tuple: (symbol, color) values used by the blinker animation.
        """
        pass
