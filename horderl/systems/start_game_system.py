"""System for handling game start events.

Consumes components:
- MovePeasantsOut
- MovePlayerToTownCenter
- SaveOnSeasonReset
"""

from __future__ import annotations

from random import choice

from engine import GameScene
from engine.components import Coordinates
from horderl.components.brains.peasant_actor import PeasantActor
from horderl.components.events.start_game_events import StartGame
from horderl.components.relationships.farmed_by import FarmedBy
from horderl.components.season_reset_listeners.move_peasants_out import (
    MovePeasantsOut,
)
from horderl.components.season_reset_listeners.move_player_to_town_center import (
    MovePlayerToTownCenter,
)
from horderl.components.season_reset_listeners.save_on_season import (
    SaveOnSeasonReset,
)
from horderl.components.serialization.save_game import SaveGame
from horderl.components.tags.peasant_tag import PeasantTag
from horderl.components.tags.town_center_flag import TownCenterFlag


def run(scene: GameScene) -> None:
    """
    Execute game start behavior for queued events.

    Args:
        scene: Active game scene with component manager access.

    Side Effects:
        - Moves peasants and player into initial positions.
        - Issues autosave requests when configured.

    """
    if not scene.cm.get(StartGame):
        return

    for _listener in scene.cm.get(MovePeasantsOut):
        _move_peasants_out(scene)
    for listener in scene.cm.get(MovePlayerToTownCenter):
        _move_player_to_town_center(scene, listener)
    for listener in scene.cm.get(SaveOnSeasonReset):
        _autosave(scene, listener)


def _move_peasants_out(scene: GameScene) -> None:
    peasants = scene.cm.get(PeasantTag)
    for peasant in peasants:
        farm_plots = scene.cm.get(
            FarmedBy,
            project=lambda x: x.entity,
            query=lambda x: x.farmer == peasant.entity,
        )
        target = choice(farm_plots)
        coords = scene.cm.get_one(Coordinates, entity=target)
        peasant_coords = scene.cm.get_one(Coordinates, entity=peasant.entity)

        peasant_coords.x = coords.x
        peasant_coords.y = coords.y

        actor = scene.cm.get_one(PeasantActor, entity=peasant.entity)
        actor.state = PeasantActor.State.FARMING


def _move_player_to_town_center(
    scene: GameScene, listener: MovePlayerToTownCenter
) -> None:
    listener._log_info("moving player to town center")
    flag = scene.cm.get(TownCenterFlag)[0]
    coord = scene.cm.get_one(Coordinates, entity=flag.entity)
    player = scene.cm.get_one(Coordinates, entity=scene.player)
    player.x = coord.x
    player.y = coord.y


def _autosave(scene: GameScene, listener: SaveOnSeasonReset) -> None:
    if not scene.config.autosave_enabled:
        listener._log_info("autosave is disabled")
        return
    scene.cm.add(SaveGame(entity=scene.player))
