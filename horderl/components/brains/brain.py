from abc import ABC
from dataclasses import dataclass

from engine import GameScene, constants
from engine.components import EnergyActor

from ..animation_controllers.blinker_animation_controller import BlinkerAnimationController


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
        blinker = scene.cm.get_one(BlinkerAnimationController, entity=self.entity)
        if blinker:
            blinker.stop(scene)
            scene.cm.delete_component(blinker)
        scene.cm.delete_component(self)
        return old_actor

    def _on_back_out(self, scene):
        pass
