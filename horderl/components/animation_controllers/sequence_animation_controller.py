from dataclasses import dataclass, field
from engine.game_scene import GameScene
from engine.logging import get_logger
from overrides import override
from typing import List

from engine.components.animation_controller import AnimationController
from horderl.components import Appearance
from horderl.components.events.delete_event import Delete


@dataclass
class SequenceAnimationController(AnimationController):
    """
    Step through a predefined sequence of (color, symbol) pairs.
    """

    timer_delay: int = 90
    sequence: List = field(default_factory=list)

    _current_step: int = 0
    _appearance: Appearance = None
    _logger = get_logger(__name__)

    @override
    def animate(self, scene: GameScene, dt_ms: int):
        if self._current_step >= len(self.sequence):
            # end of sequence, delete entity
            self._logger.debug("SequenceAnimationController sequence complete for entity %s", self.entity)
            self.stop(scene)

        self._appearance.symbol = self.sequence[self._current_step][1]
        self._appearance.color = self.sequence[self._current_step][0]
        self._current_step += 1

    @override
    def on_start(self, scene: GameScene):
        self._logger = scene.logger.get_logger(__name__)
        self._logger.debug("SequenceAnimationController starting for entity %s", self.entity)
        self._appearance = scene.cm.get_one(Appearance, entity=self.entity)

    @override
    def on_stop(self, scene: GameScene):
        self._logger.debug("SequenceAnimationController stopping for entity %s", self.entity)
