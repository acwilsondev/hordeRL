import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.component_manager import ComponentManager
from engine.components import Coordinates
from horderl.components.events.start_game_events import StartGame
from horderl.components.season_reset_listeners.move_player_to_town_center import (
    MovePlayerToTownCenter,
)
from horderl.components.tags.town_center_flag import TownCenterFlag
from horderl.systems.start_game_system import run as run_start_game


class DummyScene:
    """Minimal scene stub exposing a component manager."""

    def __init__(self) -> None:
        """Initialize the scene with a component manager."""
        self.cm = ComponentManager()
        self.player = 1


def test_start_game_system_moves_player_to_town_center():
    scene = DummyScene()
    player_coords = Coordinates(entity=scene.player, x=0, y=0)
    town_center = 2
    flag = TownCenterFlag(entity=town_center)
    town_coords = Coordinates(entity=town_center, x=5, y=7)
    mover = MovePlayerToTownCenter(entity=scene.player)
    scene.cm.add(player_coords, flag, town_coords, mover, StartGame(entity=1))

    run_start_game(scene)

    assert (player_coords.x, player_coords.y) == (5, 7)
