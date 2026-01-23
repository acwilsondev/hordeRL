from dataclasses import dataclass

from ..components.events.start_game_events import GameStartListener


@dataclass
class AnnounceGameStart(GameStartListener):
    """Tag entities that should announce the game start text."""
