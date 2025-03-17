from dataclasses import dataclass

from horderl.engine import constants

from ..tags.tag import Tag


@dataclass
class Resident(Tag):
    resident: int = constants.INVALID
    value: str = "house"
