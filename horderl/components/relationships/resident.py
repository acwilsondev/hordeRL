from dataclasses import dataclass

from engine import constants

from ..tags.tag import Tag


@dataclass
class Resident(Tag):
    resident: int = constants.INVALID
    value: str = "house"
