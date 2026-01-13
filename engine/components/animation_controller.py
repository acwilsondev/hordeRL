from abc import ABC
from dataclasses import dataclass
from overrides import override

from engine import core
from engine.components import Actor
from engine.components.updateable import Updateable
from engine.game_scene import GameScene


@dataclass
class AnimationController(Updateable, ABC):
    """
    Base class for animation effects that can be applied to entities.
    """

    SLOWEST = 100000
    ONE_SECOND = 1000
    REAL_TIME = 0

    timer_delay: int = REAL_TIME  # milliseconds between updates
    next_update: int = 0  # datetime millis for next update

    # whether to delete the entity when done, useful for one-off animations
    delete_on_complete: bool = False

    _is_animating: bool = True  # whether the animation is active
    started: bool = False

    @override
    def update(self, scene: GameScene, dt_ms: int):
        if not self._is_animating:
            # Not animating, skip
            return

        if self.next_update > core.time_ms():
            # Not yet time for next update
            return
        
        if not self.started:
            # in case we forgot to start
            self.started = True
            self.on_start(scene)

        self.next_update = core.time_ms() + self.timer_delay
        self.animate(scene, dt_ms)

    def start(self, scene: GameScene):
        """Start the animation effect."""
        self.next_update = core.time_ms() + self.timer_delay
        self._is_animating = True
        self.on_start(scene)
        self.started = True

    def stop(self, scene: GameScene):
        """Stop the animation effect."""
        self._is_animating = False
        self.on_stop(scene)
        if self.delete_on_complete:
            scene.cm.delete(self.entity)

    def animate(self, scene: GameScene, dt_ms: int):
        """Perform the animation effect. To be implemented by subclasses."""
        raise NotImplementedError(
            "Subclasses must implement the animate method."
        )

    def on_start(self, scene: GameScene):
        """Hook for when the animation starts. Can be overridden by subclasses."""
        pass

    def on_stop(self, scene: GameScene):
        """Hook for when the animation stops. Can be overridden by subclasses."""
        pass
