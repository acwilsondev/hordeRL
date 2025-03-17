from dataclasses import dataclass

from ..base_components.component import Component
from horderl.engine import constants


@dataclass
class FarmedBy(Component):
    farmer: str = constants.INVALID
