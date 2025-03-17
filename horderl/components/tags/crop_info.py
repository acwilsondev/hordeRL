from dataclasses import dataclass

from ..base_components.component import Component
from horderl.engine import constants


@dataclass
class CropInfo(Component):
    field_id: int = constants.INVALID
    farmer_id: int = constants.INVALID
