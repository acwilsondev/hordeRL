from dataclasses import dataclass

from ..tags.tag import Tag
from horderl.engine import constants


@dataclass
class Resident(Tag):
    resident: int = constants.INVALID
    value: str = "house"
