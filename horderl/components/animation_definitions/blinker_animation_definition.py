from dataclasses import dataclass
from typing import Optional, Tuple

from horderl import palettes

from .animation_definition import AnimationDefinition


@dataclass
class BlinkerAnimationDefinition(AnimationDefinition):
    """
    Store the data needed to blink an entity's appearance.
    """

    timer_delay: int = 250
    new_symbol: str = "?"
    new_color: Tuple[int, int, int] = palettes.DEBUG
    new_bg_color: Tuple[int, int, int] = palettes.BACKGROUND
    is_on: bool = False
    original_symbol: Optional[str] = None
    original_color: Optional[Tuple[int, int, int]] = None
    original_bg_color: Optional[Tuple[int, int, int]] = None
