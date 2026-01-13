# Shamelessly stolen: https://lospec.com/palette-list/fantasy-24
from typing import Any

BACKGROUND = (0, 0, 0)
GRASS = (0, 0, 0)
WALL_TREE = (0, 0, 0)
FOILAGE_C = (0, 0, 0)
GOLD = (0, 0, 0)
WHITE = (0, 0, 0)
GABRIEL_2_1 = (0, 0, 0)
SHADOW = (0, 0, 0)
FIRE = (0, 0, 0)
STRAW = (0, 0, 0)
DIRT = (0, 0, 0)
WOOD = (0, 0, 0)
MEAT = (0, 0, 0)
STONE = (0, 0, 0)
WATER = (0, 0, 0)
FRESH_BLOOD = (0, 0, 0)
LIGHT_WATER = (0, 0, 0)
HORDELING = (0, 0, 0)
# (54, 23, 12),
BLOOD = (0, 0, 0)
# (48, 15, 10)


def apply_config(config: Any) -> None:
    global BACKGROUND
    global GRASS
    global WALL_TREE
    global FOILAGE_C
    global GOLD
    global WHITE
    global GABRIEL_2_1
    global SHADOW
    global FIRE
    global STRAW
    global DIRT
    global WOOD
    global MEAT
    global STONE
    global WATER
    global FRESH_BLOOD
    global LIGHT_WATER
    global HORDELING
    global BLOOD

    BACKGROUND = config.color_background
    GRASS = config.color_grass
    WALL_TREE = config.color_wall_tree
    FOILAGE_C = config.color_normal_tree
    GOLD = config.color_gold
    WHITE = config.color_white
    GABRIEL_2_1 = config.color_peasant
    SHADOW = config.color_shadow
    FIRE = config.color_fire
    STRAW = config.color_straw
    DIRT = config.color_dirt
    WOOD = config.color_wood
    MEAT = config.color_meat
    STONE = config.color_stone
    WATER = config.color_water
    FRESH_BLOOD = config.color_fresh_blood
    LIGHT_WATER = config.color_light_water
    HORDELING = config.color_hordeling
    BLOOD = config.color_blood
