"""Deprecated settings module.

Prefer importing Config/load_config from horderl.config.
This module remains as a compatibility shim.
"""

from horderl.config import (
    Config,
    from_hex,
    get_relative_path,
    load_config,
    resource_path,
)

_DEFAULT_CONFIG = load_config(get_relative_path("options.yaml"), overrides={})

AUTOSAVE = _DEFAULT_CONFIG.autosave_enabled
GRASS_DENSITY = _DEFAULT_CONFIG.grass_density
CHARACTER_NAME = _DEFAULT_CONFIG.character_name
TORCH_RADIUS = _DEFAULT_CONFIG.torch_radius
MUSIC_ENABLED = _DEFAULT_CONFIG.music_enabled
SEED = _DEFAULT_CONFIG.world_seed

BACKGROUND = _DEFAULT_CONFIG.color_background
GRASS = _DEFAULT_CONFIG.color_grass
WALL_TREE = _DEFAULT_CONFIG.color_wall_tree
NORMAL_TREE = _DEFAULT_CONFIG.color_normal_tree
GOLD = _DEFAULT_CONFIG.color_gold
WHITE = _DEFAULT_CONFIG.color_white
GABRIEL_2_1 = _DEFAULT_CONFIG.color_peasant
SHADOW = _DEFAULT_CONFIG.color_shadow
FIRE = _DEFAULT_CONFIG.color_fire
STRAW = _DEFAULT_CONFIG.color_straw
DIRT = _DEFAULT_CONFIG.color_dirt
WOOD = _DEFAULT_CONFIG.color_wood
MEAT = _DEFAULT_CONFIG.color_meat
STONE = _DEFAULT_CONFIG.color_stone
WATER = _DEFAULT_CONFIG.color_water
FRESH_BLOOD = _DEFAULT_CONFIG.color_fresh_blood
LIGHT_WATER = _DEFAULT_CONFIG.color_light_water
HORDELING = _DEFAULT_CONFIG.color_hordeling
BLOOD = _DEFAULT_CONFIG.color_blood

FONT = _DEFAULT_CONFIG.font

SCREEN_WIDTH = _DEFAULT_CONFIG.screen_width
SCREEN_HEIGHT = _DEFAULT_CONFIG.screen_height

MAP_WIDTH = _DEFAULT_CONFIG.map_width
MAP_HEIGHT = _DEFAULT_CONFIG.map_height

BAR_WIDTH = _DEFAULT_CONFIG.bar_width
PANEL_HEIGHT = _DEFAULT_CONFIG.panel_height
PANEL_Y = _DEFAULT_CONFIG.panel_y
MSG_X = _DEFAULT_CONFIG.msg_x
MSG_WIDTH = _DEFAULT_CONFIG.msg_width
MSG_HEIGHT = _DEFAULT_CONFIG.msg_height
INVENTORY_WIDTH = _DEFAULT_CONFIG.inventory_width

FOV_ALGO = _DEFAULT_CONFIG.fov_algo
FOV_LIGHT_WALLS = _DEFAULT_CONFIG.fov_light_walls
SPAWN_FREQUENCY = _DEFAULT_CONFIG.spawn_frequency
