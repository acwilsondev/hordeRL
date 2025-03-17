from dataclasses import dataclass

from ..base_components.component import Component
from ...engine import constants


@dataclass
class FarmedBy(Component):
    farmer: str = constants.INVALID
