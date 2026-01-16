from dataclasses import dataclass

from ..abilities.ability import Ability


@dataclass
class ControlModeAbility(Ability):
    """
    Describe a control-mode ability that swaps the active controller.
    """

    control_mode_key: str = ""
    anim_symbol: str = ""
    anim_color: tuple | None = None
