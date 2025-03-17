from dataclasses import dataclass

from ..base_components.component import Component
from ..base_components.energy_actor import EnergyActor


@dataclass
class Move(Component):
    energy_cost: int = EnergyActor.HOURLY
