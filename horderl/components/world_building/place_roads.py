import random
from typing import List

from horderl.components import Coordinates
from horderl.components.events.build_world_events import BuildWorldListener
from horderl.components.house_structure import HouseStructure
from horderl.components.tags.town_center_flag import TownCenterFlag
from horderl.engine.utilities import get_3_by_3_box, get_3_by_3_square

from ...content.terrain.roads import connect_point_to_road_network, make_road


def get_town_center(house_coords, scene):
    avg_x = int(sum(c.x for c in house_coords) / len(house_coords))
    avg_y = int(sum(c.y for c in house_coords) / len(house_coords))
    all_coords = set(scene.cm.get(Coordinates, project=lambda c: (c.x, c.y)))
    while not get_3_by_3_square(avg_x, avg_y).isdisjoint(all_coords):
        avg_x += random.randint(-2, 2)
        avg_y += random.randint(-2, 2)
    return avg_x, avg_y


def connect_houses_to_road(house_coords, scene):
    for coord in house_coords:
        connect_point_to_road_network(scene, coord.position, trim_start=2)


def add_town_center(house_coords, scene):
    # Identify the town center by averaging the coords
    avg_x, avg_y = get_town_center(house_coords, scene)
    for coord in list(get_3_by_3_box(avg_x, avg_y)):
        scene.cm.add(*make_road(coord[0], coord[1])[1])
    town_center = make_road(avg_x, avg_y)
    town_center[1].append(TownCenterFlag(entity=town_center[0]))
    scene.cm.add(*town_center[1])


class PlaceRoads(BuildWorldListener):
    def on_build_world(self, scene):
        self._log_info(f"placing roads in town")
        houses: List[HouseStructure] = scene.cm.get(
            HouseStructure, project=lambda hs: hs.house_id
        )
        house_coords: List[Coordinates] = [
            scene.cm.get_one(Coordinates, entity=house) for house in houses
        ]

        add_town_center(house_coords, scene)
        connect_houses_to_road(house_coords, scene)
        self.draw_road_across_map(scene)

    def draw_road_across_map(self, scene):
        self._log_info(f"placing highway")
        start = (0, random.randint(2, scene.config.map_width - 3))
        connect_point_to_road_network(scene, start)
        end = (
            scene.config.map_width - 1,
            random.randint(2, scene.config.map_height - 3),
        )
        connect_point_to_road_network(scene, end)
