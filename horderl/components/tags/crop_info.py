from dataclasses import dataclass

from horderl.engine import constants

from ..base_components.component import Component


@dataclass
class CropInfo(Component):
    field_id: int = constants.INVALID
    farmer_id: int = constants.INVALID
