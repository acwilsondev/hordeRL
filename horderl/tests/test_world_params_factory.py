from types import SimpleNamespace

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
)
from horderl.systems.world_building import params_factory


def test_get_seed_uses_random_when_configured(monkeypatch):
    config = SimpleNamespace(world_seed="RANDOM")

    monkeypatch.setattr(params_factory.time, "time_ns", lambda: 12345)

    assert params_factory.get_seed(config) == 12345


def test_get_seed_uses_configured_value():
    config = SimpleNamespace(world_seed=999)

    assert params_factory.get_seed(config) == 999


def test_get_plains_params_uses_defaults():
    config = SimpleNamespace(world_seed=42)

    params = params_factory.get_plains_params(entity=1, config=config)

    assert params.biome == "Plains"
    assert params.world_seed == 42
    assert params.lakes == DEFAULT_LAKES
    assert params.copse == DEFAULT_COPSE


def test_get_forest_params_sets_forest_tuning():
    config = SimpleNamespace(world_seed=84)

    params = params_factory.get_forest_params(entity=2, config=config)

    assert params.biome == "Forest"
    assert params.world_seed == 84
    assert params.copse == DEFAULT_COPSE * 20
    assert params.flower_fields == DEFAULT_FLOWERS // 2
    assert params.flower_proliferation == DEFAULT_FLOWER_PROLIFERATION / 2
    assert params.tree_cut_anger == DEFAULT_TREE_CUT_ANGER * 2


def test_get_mountain_params_sets_mountain_tuning():
    config = SimpleNamespace(world_seed=21)

    params = params_factory.get_mountain_params(entity=3, config=config)

    assert params.biome == "Mountain"
    assert params.world_seed == 21
    assert params.copse == DEFAULT_COPSE // 2
    assert params.copse_proliferation == DEFAULT_COPSE_PROLIFERATION / 2
    assert params.rock_fields == DEFAULT_ROCKS * 40
    assert params.rocks_proliferation == DEFAULT_ROCKS_PROLIFERATION * 2
    assert params.lakes == 0
    assert params.temperature_modifier == DEFAULT_TEMPERATURE_MODIFIER - 5
    assert params.river_rapids == DEFAULT_RIVER_RAPIDS // 5


def test_get_swamp_params_sets_swamp_tuning():
    config = SimpleNamespace(world_seed=7)

    params = params_factory.get_swamp_params(entity=4, config=config)

    assert params.biome == "Swamp"
    assert params.world_seed == 7
    assert params.copse == DEFAULT_COPSE * 10
    assert params.copse_proliferation == DEFAULT_COPSE_PROLIFERATION / 2
    assert params.lakes == DEFAULT_LAKES * 100
    assert params.lake_proliferation == DEFAULT_LAKE_PROLIFERATION / 2
    assert params.rocks_proliferation == 0
    assert params.temperature_modifier == DEFAULT_TEMPERATURE_MODIFIER + 5
    assert params.is_water_swampy is True


def test_get_tundra_params_sets_tundra_tuning():
    config = SimpleNamespace(world_seed=11)

    params = params_factory.get_tundra_params(entity=5, config=config)

    assert params.biome == "Tundra"
    assert params.world_seed == 11
    assert params.copse == 0
    assert params.rock_fields == DEFAULT_ROCKS * 10
    assert params.rocks_proliferation == DEFAULT_ROCKS_PROLIFERATION * 2
    assert params.lakes == DEFAULT_LAKES * 100
    assert params.lake_proliferation == DEFAULT_LAKE_PROLIFERATION / 2
    assert params.temperature_modifier == DEFAULT_TEMPERATURE_MODIFIER - 20
    assert params.is_water_swampy is True
