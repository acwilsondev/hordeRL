from dataclasses import dataclass
from typing import Callable

from ..abilities.ability import Ability


@dataclass
class ControlModeAbility(Ability):
    """
    Describe a control-mode ability that swaps the active controller.
    """

    mode_factory: Callable | None = None
    anim_symbol: str = ""
    anim_color: tuple | None = None
