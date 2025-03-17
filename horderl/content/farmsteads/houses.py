import logging
import random
from typing import Set

from horderl import settings
from horderl.components import Coordinates
from horderl.components.house_structure import HouseStructure
from horderl.content.allies.peasants import make_peasant
from horderl.content.farmsteads.farms import make_farm_plot
from horderl.content.farmsteads.floorboard import make_floorboard
from horderl.content.farmsteads.walls import make_wall
from horderl.engine import constants, core, palettes
from horderl.engine.types import ComplexEntity, EntityId
from horderl.engine.utilities import get_3_by_3_square, get_box


def place_farmstead(scene) -> EntityId:
    """Place a new house, farm, peasant, and connect them to the road network."""
    coords: Set[Coordinates] = {
        (coord.x, coord.y) for coord in scene.cm.get(Coordinates)
    }

    x, y = _get_point()
    footprint = get_3_by_3_square(x, y)

    attempts = 100
    while not coords.isdisjoint(footprint) and attempts > 0:
        attempts -= 1
        x, y = _get_point()
        footprint = get_3_by_3_square(x, y)

    if not attempts:
        logging.warning("Failed to place farmstead.")
        return constants.INVALID

    house = _add_house(scene, x, y)
    return house


def _make_house(root_id: EntityId, resident, x, y) -> ComplexEntity:
    floorboard = make_floorboard(root_id, x, y, resident)

    upper_left = make_wall(root_id, x - 1, y - 1, piece="ul")
    upper_middle = make_wall(root_id, x, y - 1, piece="um")
    upper_right = make_wall(root_id, x + 1, y - 1, piece="ur")
    middle_left = make_wall(root_id, x - 1, y, piece="ml")
    middle_right = make_wall(root_id, x + 1, y, piece="mr")
    bottom_left = make_wall(root_id, x - 1, y + 1, piece="bl")
    bottom_middle = make_wall(root_id, x, y + 1, piece="bm")
    bottom_right = make_wall(root_id, x + 1, y + 1, piece="br")

    structure = HouseStructure(
        entity=root_id,
        house_id=root_id,
        upper_left=upper_left[0],
        upper_middle=upper_middle[0],
        upper_right=upper_right[0],
        middle_left=middle_left[0],
        middle_right=middle_right[0],
        bottom_left=bottom_left[0],
        bottom_middle=bottom_middle[0],
        bottom_right=bottom_right[0],
    )

    floorboard[1].append(structure)

    return (
        root_id,
        [
            upper_left,
            upper_middle,
            upper_right,
            middle_left,
            floorboard,
            middle_right,
            bottom_left,
            bottom_middle,
            bottom_right,
        ],
    )


def _make_peasant_home(x, y) -> ComplexEntity:
    house_id = core.get_id()
    peasant = make_peasant(house_id, x, y)
    house = _make_house(house_id, peasant[0], x, y)
    house[1].append(peasant)
    return house


def _add_house(scene, x, y) -> EntityId:
    house: ComplexEntity = _make_peasant_home(x, y)
    for entity in house[1]:
        scene.cm.add(*entity[1])

    possible_coords = [x for x in get_box((x - 3, y - 3), (x + 2, y + 2))]
    random.shuffle(possible_coords)
    finalized_plot = None
    while possible_coords and not finalized_plot:
        plot_corner = possible_coords.pop()
        corner_x = plot_corner[0]
        corner_y = plot_corner[1]
        farm_plot = get_box((corner_x, corner_y), (corner_x + 1, corner_y + 1))

        coords = {(coord.x, coord.y) for coord in scene.cm.get(Coordinates)}
        if farm_plot.isdisjoint(coords):
            # safe to reuse old coords, can't overlap with this home
            finalized_plot = [x for x in farm_plot]

    if finalized_plot:
        peasant = house[-1][-1]
        peasant_id = peasant[0]

        crop_color = random.choice(
            [
                palettes.FIRE,
                palettes.FOILAGE_C,
                palettes.FRESH_BLOOD,
                palettes.GOLD,
            ]
        )
        for point in finalized_plot:
            plot = make_farm_plot(point[0], point[1], peasant_id, crop_color)
            scene.cm.add(*plot[1])
    return house[0]


def _get_point():
    x = random.randint(5, settings.MAP_WIDTH - 5)
    y = random.randint(5, settings.MAP_HEIGHT - 5)
    return x, y
