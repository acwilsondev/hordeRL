from dataclasses import dataclass

from horderl.engine.components.component import Component
from horderl.components.actors.energy_actor import EnergyActor


@dataclass
class Move(Component):
    energy_cost: int = EnergyActor.HOURLY
