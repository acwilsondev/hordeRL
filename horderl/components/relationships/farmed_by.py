from dataclasses import dataclass

from horderl.engine import constants
from horderl.engine.components.component import Component


@dataclass
class FarmedBy(Component):
    farmer: str = constants.INVALID
