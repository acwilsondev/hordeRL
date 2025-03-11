from dataclasses import dataclass

from .. import Appearance
from ..base_components.timed_actor import TimedActor
from ...engine import palettes


@dataclass
class AnimationBlinker(TimedActor):
    """Flip the colors back and forth."""

    timer_delay: int = 250
    original_symbol: str = None
    original_color: tuple = None
    original_bg_color: tuple = None

    new_symbol: str = "X"
    new_color: tuple = palettes.GOLD
    new_bg_color: tuple = palettes.BACKGROUND

    is_on: bool = False
    is_animating: bool = True

    def act(self, scene):
        if not self.is_animating:
            return
        appearance = scene.cm.get_one(Appearance, entity=self.entity)
        if self.is_on:
            next_symbol = self.original_symbol or appearance.symbol
            next_color = self.original_color or appearance.color
            next_bg_color = self.original_bg_color or appearance.bg_color
            appearance.set_appearance(next_symbol, next_color, next_bg_color)
        else:
            self.original_symbol = appearance.symbol
            self.original_color = appearance.color
            self.original_bg_color = appearance.bg_color
            appearance.set_appearance(
                self.new_symbol, self.new_color, self.new_bg_color
            )
        self.is_on = not self.is_on
        self.pass_turn()

    def stop(self, scene):
        appearance = scene.cm.get_one(Appearance, entity=self.entity)
        appearance.symbol = self.original_symbol
        appearance.color = self.original_color
        self.is_animating = False
