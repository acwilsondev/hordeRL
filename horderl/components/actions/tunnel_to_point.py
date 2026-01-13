from dataclasses import dataclass
from typing import Tuple

from engine import constants
from engine.components import Coordinates, EnergyActor
from horderl.content.terrain.hole import make_hole


@dataclass
class TunnelToPoint(EnergyActor):
    """
    Instance of a live attack.
    """

    target: int = constants.INVALID
    point: Tuple[int, int] = (0, 0)

    def act(self, scene):
        self._log_info(f"tunnelling to point {self.point}")
        coords = scene.cm.get_one(Coordinates, entity=self.entity)
        coords.x = self.point[0]
        coords.y = self.point[1]
        scene.cm.add(*make_hole(coords.x, coords.y)[1])
        scene.cm.delete_component(self)
