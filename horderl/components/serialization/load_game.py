from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class LoadGame(Component):
    """
    Hold configuration for a load game request.

    Attributes:
        file_name (str): Path to the save file that should be loaded.

    """

    file_name: str = ""
