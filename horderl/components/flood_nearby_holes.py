from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class FloodHolesState(Component):
    """
    Record flood-fill timing state for the flood holes system.
    """

    is_active: bool = False
    next_step_time_ms: int = 0
    step_delay_ms: int = 500
