from dataclasses import dataclass

from engine import constants
from horderl.components.actors.energy_actor import EnergyActor
from horderl.components.brains.painters.painter_brain import PainterBrain
from horderl.content.enemies.juvenile import make_juvenile


@dataclass
class PlaceHordelingController(PainterBrain):
    energy_cost: int = EnergyActor.INSTANT
    cursor: int = constants.INVALID

    def paint_one(self, scene, position):
        return make_juvenile(position[0], position[1])[1]
