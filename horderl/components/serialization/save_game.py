from dataclasses import dataclass, field
from typing import Dict

from engine.components.component import Component


@dataclass
class SaveGame(Component):
    """
    Hold configuration for a save game request.

    This component does not perform IO itself. Systems are responsible for
    translating this configuration into an actual save operation.

    Attributes:
        extra (Dict): Optional additional data to include in the save file,
                      provided as a dictionary that gets merged with the
                      serialized game state.

    """

    extra: Dict = field(default_factory=dict)
