from dataclasses import dataclass

from horderl.components.brains.painters.painter_brain import PainterBrain
from horderl.content.getables.gold import make_gold_nugget
from horderl.engine import constants
from horderl.engine.components.energy_actor import EnergyActor


@dataclass
class PlaceGoldController(PainterBrain):
    energy_cost: int = EnergyActor.INSTANT
    cursor: int = constants.INVALID

    def paint_one(self, scene, position):
        return make_gold_nugget(position[0], position[1])[1]
