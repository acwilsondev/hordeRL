"""System that updates weather state in response to calendar events."""

from __future__ import annotations

import random
from typing import Iterable, List, TypeVar

from engine import GameScene, core
from engine.logging import get_logger
from horderl.components.events.new_day_event import DayBegan
from horderl.components.events.start_game_events import StartGame
from horderl.components.season_reset_listeners.reset_season import ResetSeason
from horderl.components.tags.ice_tag import IceTag
from horderl.components.tags.water_tag import WaterTag
from horderl.components.weather.freeze_water import FreezeWater
from horderl.components.weather.snow_fall import SnowFall
from horderl.components.weather.weather import Weather
from horderl.components.world_building.world_parameters import WorldParameters
from horderl.content.terrain.water import freeze, thaw
from horderl.systems.utilities import consume_energy, is_energy_ready


def run(scene: GameScene) -> None:
    """
    Update weather state and apply weather-related effects.

    Args:
        scene: Active game scene with the component manager and messaging.

    Components Consumed:
        - Weather stored on the calendar entity.
        - DayBegan, ResetSeason, and StartGame events.
        - FreezeWater and SnowFall weather actor components.
        - WaterTag and IceTag for freezing/thawing tiles.

    Side Effects:
        - Updates the Weather component's seasonal norm and temperature.
        - Sends a message if the temperature crosses freezing.
        - Mutates terrain tiles (freeze/thaw) and updates the play window.
        - Consumes energy for weather actors via consume_energy().

    """
    weather = _get_weather(scene)
    if not weather:
        return

    if scene.cm.get(StartGame):
        _set_seasonal_norm(scene, weather, "Spring")

    for season_event in _calendar_events(scene.cm.get(ResetSeason)):
        _set_seasonal_norm(scene, weather, season_event.season)

    for day_event in _calendar_events(scene.cm.get(DayBegan)):
        _set_temperature(scene, weather)

    _run_freeze_water(scene, weather)
    _run_snow_fall(scene, weather)


EventType = TypeVar("EventType")


def _calendar_events(events: Iterable[EventType]) -> List[EventType]:
    calendar_id = core.get_id("calendar")
    return [event for event in events if event.entity == calendar_id]


def _get_weather(scene: GameScene) -> Weather | None:
    # Weather is expected to be stored on the calendar entity.
    return scene.cm.get_one(Weather, entity=core.get_id("calendar"))


def _set_seasonal_norm(
    scene: GameScene, weather: Weather, season: str
) -> None:
    seasonal_temp = weather.seasonal_temperatures[season]
    world_params = scene.cm.get_one(
        WorldParameters, entity=core.get_id("world")
    )
    modifier = world_params.temperature_modifier if world_params else 0
    weather.seasonal_norm = seasonal_temp + modifier
    weather._log_info(f"set normal temp {weather.seasonal_norm}")
    _set_temperature(scene, weather)


def _set_temperature(scene: GameScene, weather: Weather) -> None:
    previous_temp = weather.temperature
    weather.temperature = weather.seasonal_norm + random.randint(
        -weather.daily_variation, weather.daily_variation
    )
    weather._log_info(f"set daily temp {weather.temperature}")
    _notify_freezing_threshold(scene, previous_temp, weather.temperature)


def _notify_freezing_threshold(
    scene: GameScene, previous_temp: int, current_temp: int
) -> None:
    if previous_temp >= 0 > current_temp:
        scene.message("It is freezing outside.")
    elif previous_temp <= 0 < current_temp:
        scene.message("The weather warmed up.")


def _run_freeze_water(scene: GameScene, weather: Weather) -> None:
    # Uses weather temperature to freeze/thaw terrain tiles.
    logger = get_logger(__name__)
    for freeze_water in scene.cm.get(FreezeWater):
        if not is_energy_ready(freeze_water):
            continue
        if weather.temperature < 0:
            count = max(weather.temperature * -1, 5)
            logger.debug("freezing %s tiles", count)
            _freeze_tiles(scene, count)
        else:
            count = max(weather.temperature, 5)
            logger.debug("thawing %s tiles", count)
            _thaw_tiles(scene, count)
        consume_energy(freeze_water)


def _freeze_tiles(scene: GameScene, count: int) -> None:
    # Randomizes water tiles to freeze.
    waters = scene.cm.get(WaterTag, project=lambda wt: wt.entity)
    if not waters:
        return
    count = min(count, len(waters))
    random.shuffle(waters)
    for water in waters[:count]:
        freeze(scene, water)


def _thaw_tiles(scene: GameScene, count: int) -> None:
    # Randomizes ice tiles to thaw.
    ices = scene.cm.get(IceTag, project=lambda it: it.entity)
    if not ices:
        return
    count = min(count, len(ices))
    random.shuffle(ices)
    for ice in ices[:count]:
        thaw(scene, ice)


def _run_snow_fall(scene: GameScene, weather: Weather) -> None:
    # Adds snow or grass based on the current temperature.
    for snow_fall in scene.cm.get(SnowFall):
        if not is_energy_ready(snow_fall):
            continue
        if weather.temperature < 5:
            for _ in range(10 - weather.temperature):
                scene.play_window.add_snow()
        else:
            for _ in range(weather.temperature):
                scene.play_window.add_grass()
        consume_energy(snow_fall)
