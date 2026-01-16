from dataclasses import dataclass
from engine.components.component import Component


@dataclass
class WorldbuildingControl(Component):
    """
    Options for controlling system execution.
    """

    # we have created a worldbuilding biome dialog and are waiting for user input
    world_parameters_selecting: bool = False
    # the user has selected world parameters via the biome dialog
    world_parameters_selected: bool = False
