from dataclasses import dataclass
from engine.logging import get_logger
from overrides import override

from engine.components import Coordinates
from engine.components.animation_controller import AnimationController
from engine.game_scene import GameScene
from horderl.components.path_node import PathNode


@dataclass
class PathAnimationController(AnimationController):
    timer_delay: int = 30

    # Usually for one-shot animations
    delete_on_complete: bool = True

    _logger= get_logger(__name__)
    _coordinates: Coordinates = None  # coordinates component for the entity
    _current_step: int = 0  # step in the path

    @override
    def animate(self, scene: GameScene, dt_ms: int):
        path_nodes = scene.cm.get_all(PathNode, entity=self.entity)
        try:
            next_node = next(
                p for p in path_nodes if p.step == self._current_step
            )

            self._coordinates.x = next_node.x
            self._coordinates.y = next_node.y

            self._current_step += 1
        except StopIteration:
            self.stop(scene)

    @override
    def on_start(self, scene: GameScene):
        self._logger.debug(
            "PathAnimationController starting for entity %s", self.entity
        )
        self._coordinates = scene.cm.get_one(Coordinates, entity=self.entity)

    @override
    def on_stop(self, scene: GameScene):
        self._logger.debug(
            "PathAnimationController stopping for entity %s", self.entity
        )
