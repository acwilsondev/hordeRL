from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class StartMusic(Component):
    """
    Configure the music track to play at game start or season reset.
    """

    track_id: str = "town"
