from abc import ABC
from dataclasses import dataclass

from engine import GameScene, constants
from engine.components import EnergyActor

from ..animation_definitions.blinker_animation_definition import (
    BlinkerAnimationDefinition,
)


@dataclass
class Brain(EnergyActor, ABC):
    # Establish a brain stack
    old_brain: int = constants.INVALID

    def swap(self, scene: GameScene, new_brain: "Brain") -> None:
        """
        Swap this brain with a new brain.
        """
        new_brain.old_brain = self.id
        scene.cm.stash_component(self.id)
        scene.cm.add(new_brain)

    def back_out(self, scene):
        self._on_back_out(scene)
        old_actor = scene.cm.unstash_component(self.old_brain)
        # TODO not sure if this is a great place for this
        blinker = scene.cm.get_one(
            BlinkerAnimationDefinition, entity=self.entity
        )
        if blinker:
            blinker.is_animating = False
            blinker.remove_on_stop = True
        scene.cm.delete_component(self)
        return old_actor

    def _on_back_out(self, scene):
        pass
