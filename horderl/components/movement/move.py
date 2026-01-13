from dataclasses import dataclass

from engine.components.component import Component
from engine.components import EnergyActor


@dataclass
class Move(Component):
    energy_cost: int = EnergyActor.HOURLY
