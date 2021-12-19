from dataclasses import dataclass
from random import choice

from components import Coordinates
from components.game_start_listeners.game_start_listener import GameStartListener
from components.relationships.farmed_by import FarmedBy
from components.season_reset_listeners.seasonal_actor import SeasonResetListener
from components.tags.peasant_tag import PeasantTag

moves = [
    (-2, -2), (0, -2), (2, -2),
    (-2, 0), (2, 0),
    (-2, 2), (0, 2), (2, 2)

]


def _move_peasants_out(scene):
    peasants = scene.cm.get(PeasantTag)
    for peasant in peasants:
        farm_plots = scene.cm.get(
            FarmedBy,
            project=lambda x: x.entity,
            query=lambda x: x.farmer == peasant.entity
        )
        target = choice(farm_plots)
        coords = scene.cm.get_one(Coordinates, entity=target)
        peasant_coords = scene.cm.get_one(Coordinates, entity=peasant.entity)

        peasant_coords.x = coords.x
        peasant_coords.y = coords.y


@dataclass
class MovePeasantsOut(SeasonResetListener, GameStartListener):
    """Move the peasants out of their houses."""
    def on_season_reset(self, scene):
        _move_peasants_out(scene)

    def on_game_start(self, scene):
        _move_peasants_out(scene)
