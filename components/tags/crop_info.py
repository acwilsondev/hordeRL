from dataclasses import dataclass

from components.base_components.component import Component
from engine import constants


@dataclass
class CropInfo(Component):
    field_id: int = constants.INVALID
    farmer_id: int = constants.INVALID
