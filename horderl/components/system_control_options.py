from dataclasses import dataclass
from engine.components.component import Component


@dataclass
class SystemControlOptions(Component):
    """
    Options for controlling system execution.
    """

    world_parameters_selected: bool = False
    world_parameters_selecting: bool = False
    world_build_complete: bool = False
    skip_world_building: bool = False
