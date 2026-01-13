import random
from dataclasses import dataclass

from overrides import override

from engine.components.animation_controller import AnimationController
from engine.game_scene import GameScene
from engine.logging import get_logger
from horderl import palettes
from horderl.components import Appearance


@dataclass
class RandomizedBlinkerAnimationController(AnimationController):
    """
    Flip the appearance back and forth.
    """

    # Time between blinks in milliseconds
    min_timer_delay: int = 100
    max_timer_delay: int = 500

    # New appearance when "on"
    new_symbol: str = "?"
    new_color: tuple = palettes.DEBUG
    new_bg_color: tuple = palettes.BACKGROUND

    _is_on: bool = False  # whether currently in "on" state
    _appearance: Appearance = None
    _logger = get_logger(__name__)

    # Stored original appearance to restore later
    _original_symbol: str = None
    _original_color: tuple = None
    _original_bg_color: tuple = None

    @override
    def animate(self, scene: GameScene, dt_ms: int):
        if not self._appearance:
            self._logger.error(
                "RandomizedBlinkerAnimationController has no Appearance component to animate"
            )
            return
        if self._is_on:
            self._appearance.set_appearance(
                self.new_symbol, self.new_color, self.new_bg_color
            )
        else:
            self._appearance.set_appearance(
                self._original_symbol,
                self._original_color,
                self._original_bg_color,
            )
        self._is_on = not self._is_on
        # Randomize the timer delay for the next blink
        self.timer_delay = random.randint(
            self.min_timer_delay, self.max_timer_delay
        )

    @override
    def on_start(self, scene: GameScene):
        self._logger.debug("BlinkerAnimationController starting")
        if self._appearance is None:
            self._appearance = scene.cm.get_one(Appearance, entity=self.entity)
            if not self._appearance:
                raise ValueError(
                    "RandomizedBlinkerAnimationController requires an Appearance component"
                )

        self._original_bg_color = self._appearance.bg_color
        self._original_color = self._appearance.color
        self._original_symbol = self._appearance.symbol

    @override
    def on_stop(self, scene: GameScene):
        self._logger.debug(
            "BlinkerAnimationController stopping, resetting appearance"
        )

        self._appearance.bg_color = self._original_bg_color
        self._appearance.color = self._original_color
        self._appearance.symbol = self._original_symbol
