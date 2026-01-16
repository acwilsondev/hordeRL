"""
Marker component for triggering the debug menu system.
"""

from dataclasses import dataclass

from engine.components import EnergyActor


@dataclass
class ShowDebug(EnergyActor):
    """
    Marker component that requests the debug menu to be displayed.

    The component is lightweight and contains no scene mutations. Systems
    are responsible for interpreting it and presenting the debug UI.

    Attributes:
        energy_cost (int): Energy consumed when the debug menu is triggered.
    """

    energy_cost: int = EnergyActor.INSTANT
