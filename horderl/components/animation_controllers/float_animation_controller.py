import random
from dataclasses import dataclass
from engine.logging import get_logger
from overrides import override

from engine.components import Coordinates
from engine.components.animation_controller import AnimationController
from engine.game_scene import GameScene


@dataclass
class FloatAnimationController(AnimationController):
    """
    Randomly float up or right.
    """

    timer_delay: int = 125
    duration: int = 10

    # This effect is usually used for popups that should be removed after
    delete_on_complete: bool = True

    # private members
    _coordinates: Coordinates = None
    _logger = get_logger(__name__)

    @override
    def animate(self, scene: GameScene, dt_ms: int):
        up_or_over = random.choice([(0, -1), (1, 0)])
        self._coordinates.x += up_or_over[0]
        self._coordinates.y += up_or_over[1]

        if (
            self._coordinates.x >= scene.config.map_width
            or self._coordinates.y <= 0
        ):
            # out of bounds, delete
            self._logger.debug(
                "FloatAnimationController out of bounds for entity %s",
                self.entity,
            )
            self.stop(scene)

        self.duration -= 1
        if self.duration < 0:
            self._logger.debug(
                "FloatAnimationController duration complete for entity %s",
                self.entity,
            )
            self.stop(scene)

    @override
    def on_start(self, scene: GameScene):
        self._logger.debug(
            "FloatAnimationController starting for entity %s", self.entity
        )
        self._coordinates = scene.cm.get_one(Coordinates, entity=self.entity)

    @override
    def on_stop(self, scene: GameScene):
        self._logger.debug(
            "FloatAnimationController stopping for entity %s", self.entity
        )
        if self.delete_on_complete:
            scene.cm.delete(self.entity)
