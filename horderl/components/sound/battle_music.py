from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class BattleMusic(Component):
    """
    Configure the music track to play when a battle begins.
    """

    track_id: str = "battle"
