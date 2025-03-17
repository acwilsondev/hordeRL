from dataclasses import dataclass
from random import choice

from horderl.components import Coordinates
from horderl.components.brains.peasant_actor import PeasantActor
from horderl.components.events.start_game_events import GameStartListener
from horderl.components.relationships.farmed_by import FarmedBy
from horderl.components.season_reset_listeners.seasonal_actor import \
    SeasonResetListener
from horderl.components.tags.peasant_tag import PeasantTag

moves = [(-2, -2), (0, -2), (2, -2), (-2, 0), (2, 0), (-2, 2), (0, 2), (2, 2)]


def _move_peasants_out(scene, season):
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

        if season != "Winter":
            actor.state = PeasantActor.State.FARMING
        else:
            actor.state = PeasantActor.State.WANDERING


@dataclass
class MovePeasantsOut(SeasonResetListener, GameStartListener):
    """Move the peasants out of their houses."""

    def on_season_reset(self, scene, season):
        _move_peasants_out(scene, season)

    def on_game_start(self, scene):
        _move_peasants_out(scene, "Spring")
