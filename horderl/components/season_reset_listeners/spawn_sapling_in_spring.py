import random
from dataclasses import dataclass

from engine.components import Coordinates
from engine.utilities import get_3_by_3_box
from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)
from horderl.components.tags.tree_tag import TreeTag
from horderl.components.weather.weather import Weather
from horderl.content.terrain.saplings import make_sapling
from horderl.systems.brain_system import is_buildable


@dataclass
class SpawnSaplingInSpring(SeasonResetListener):
    """
    Cause trees to spawn saplings.
    """

    # Attaches to the calendar- if attached to individual trees, will cause a circular dependency with saplings.

    def on_season_reset(self, scene, season):
        self._log_info(f"triggered")
        weather = scene.cm.get(Weather)
        if weather:
            weather = weather[0]
        else:
            self._log_warning(f"no weather found")
            return

        tree_coords = [
            scene.cm.get_one(Coordinates, entity=tt.entity)
            for tt in scene.cm.get(TreeTag)
            if random.randint(0, 500) < weather.seasonal_norm
        ]

        count = 0
        for coords in tree_coords:
            count += 1
            x = coords.x
            y = coords.y
            plantable_tiles = [
                (x2, y2)
                for x2, y2 in get_3_by_3_box(x, y)
                if is_buildable(scene, x2, y2)
            ]
            target_tile = random.choice(plantable_tiles)
            scene.cm.add(*make_sapling(target_tile[0], target_tile[1])[1])
        self._log_info(f"added {count} saplings")
