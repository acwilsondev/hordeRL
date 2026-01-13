from dataclasses import dataclass

from horderl.components.actors.energy_actor import EnergyActor
from horderl.engine.components.component import Component


@dataclass
class Move(Component):
    energy_cost: int = EnergyActor.HOURLY
