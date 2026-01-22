"""Factories for constructing world-building parameter presets."""

from __future__ import annotations

import time

from horderl.components.world_building.world_parameters import (
    DEFAULT_COPSE,
    DEFAULT_COPSE_PROLIFERATION,
    DEFAULT_FLOWER_PROLIFERATION,
    DEFAULT_FLOWERS,
    DEFAULT_LAKE_PROLIFERATION,
    DEFAULT_LAKES,
    DEFAULT_RIVER_RAPIDS,
    DEFAULT_ROCKS,
    DEFAULT_ROCKS_PROLIFERATION,
    DEFAULT_TEMPERATURE_MODIFIER,
    DEFAULT_TREE_CUT_ANGER,
    WorldParameters,
)


def get_seed(config) -> int | str:
    """Return the world seed based on configuration.

    Args:
        config: Configuration object with a ``world_seed`` attribute. The
            attribute may be the string "RANDOM" or a specific seed value.

    Returns:
        The configured seed value, or a nanosecond timestamp when "RANDOM" is
        selected.

    Side effects:
        - Reads the current system time when the seed is random.

    Raised errors:
        None.

    Invariants:
        - Returned values are usable as ``WorldParameters.world_seed`` inputs.
    """
    return (
        time.time_ns() if config.world_seed == "RANDOM" else config.world_seed
    )


def get_plains_params(entity, config) -> WorldParameters:
    """Construct default plains parameters for world generation.

    Args:
        entity: Entity ID that will own the resulting ``WorldParameters``.
        config: Configuration object used to derive the world seed.

    Returns:
        A ``WorldParameters`` instance configured for the plains biome.

    Side effects:
        - Reads the system time if the config requests a random seed.

    Raised errors:
        None.

    Invariants:
        - Uses default biome tuning values for the plains preset.
    """
    return WorldParameters(entity=entity, world_seed=get_seed(config))


def get_forest_params(entity, config) -> WorldParameters:
    """Construct forest parameters for world generation.

    Args:
        entity: Entity ID that will own the resulting ``WorldParameters``.
        config: Configuration object used to derive the world seed.

    Returns:
        A ``WorldParameters`` instance configured for the forest biome.

    Side effects:
        - Reads the system time if the config requests a random seed.

    Raised errors:
        None.

    Invariants:
        - Boosts tree density and reduces flower prevalence versus plains.
    """
    return WorldParameters(
        biome="Forest",
        entity=entity,
        world_seed=get_seed(config),
        copse=DEFAULT_COPSE * 20,
        flower_fields=DEFAULT_FLOWERS // 2,
        flower_proliferation=DEFAULT_FLOWER_PROLIFERATION / 2,
        tree_cut_anger=DEFAULT_TREE_CUT_ANGER * 2,
    )


def get_mountain_params(entity, config) -> WorldParameters:
    """Construct mountain parameters for world generation.

    Args:
        entity: Entity ID that will own the resulting ``WorldParameters``.
        config: Configuration object used to derive the world seed.

    Returns:
        A ``WorldParameters`` instance configured for the mountain biome.

    Side effects:
        - Reads the system time if the config requests a random seed.

    Raised errors:
        None.

    Invariants:
        - Emphasizes rock fields, lowers temperature, and reduces forests.
    """
    return WorldParameters(
        entity=entity,
        biome="Mountain",
        world_seed=get_seed(config),
        copse=DEFAULT_COPSE // 2,
        copse_proliferation=DEFAULT_COPSE_PROLIFERATION / 2,
        rock_fields=DEFAULT_ROCKS * 40,
        rocks_proliferation=DEFAULT_ROCKS_PROLIFERATION * 2,
        lakes=0,
        temperature_modifier=DEFAULT_TEMPERATURE_MODIFIER - 5,
        river_rapids=DEFAULT_RIVER_RAPIDS // 5,
    )


def get_swamp_params(entity, config) -> WorldParameters:
    """Construct swamp parameters for world generation.

    Args:
        entity: Entity ID that will own the resulting ``WorldParameters``.
        config: Configuration object used to derive the world seed.

    Returns:
        A ``WorldParameters`` instance configured for the swamp biome.

    Side effects:
        - Reads the system time if the config requests a random seed.

    Raised errors:
        None.

    Invariants:
        - Increases lakes and warmth, marks water as swampy.
    """
    return WorldParameters(
        entity=entity,
        biome="Swamp",
        world_seed=get_seed(config),
        copse=DEFAULT_COPSE * 10,
        copse_proliferation=DEFAULT_COPSE_PROLIFERATION / 2,
        lakes=DEFAULT_LAKES * 100,
        lake_proliferation=DEFAULT_LAKE_PROLIFERATION / 2,
        rocks_proliferation=0,
        temperature_modifier=DEFAULT_TEMPERATURE_MODIFIER + 5,
        is_water_swampy=True,
    )


def get_tundra_params(entity, config) -> WorldParameters:
    """Construct tundra parameters for world generation.

    Args:
        entity: Entity ID that will own the resulting ``WorldParameters``.
        config: Configuration object used to derive the world seed.

    Returns:
        A ``WorldParameters`` instance configured for the tundra biome.

    Side effects:
        - Reads the system time if the config requests a random seed.

    Raised errors:
        None.

    Invariants:
        - Eliminates trees, increases rock fields, and lowers temperature.
    """
    return WorldParameters(
        entity=entity,
        biome="Tundra",
        world_seed=get_seed(config),
        copse=0,
        rock_fields=DEFAULT_ROCKS * 10,
        rocks_proliferation=DEFAULT_ROCKS_PROLIFERATION * 2,
        lakes=DEFAULT_LAKES * 100,
        lake_proliferation=DEFAULT_LAKE_PROLIFERATION / 2,
        temperature_modifier=DEFAULT_TEMPERATURE_MODIFIER - 20,
        is_water_swampy=True,
    )
